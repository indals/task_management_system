from app.models.task import Task
from app.models.task_comment import TaskComment
from app.models.user import User
from app.models.project import Project
from app.models.sprint import Sprint
from app.models.notification import Notification
from app.models.time_log import TimeLog
from app import db
from app.models.enums import TaskStatus, TaskPriority, TaskType, NotificationType
from datetime import datetime
import json

class TaskService:
    @staticmethod
    def create_task(dto, user_id):
        """Create a new task with enhanced IT features."""
        try:
            user = User.query.get_or_404(user_id)

            # Validate project access if provided
            project_id = dto.get('project_id')
            if project_id:
                project = Project.query.get_or_404(project_id)
                if not user.has_project_permission(project_id, 'create_tasks') and project.owner_id != user_id:
                    return {'error': 'Insufficient permissions to create task in this project'}, 403

            # Convert enums
            try:
                priority = TaskPriority[dto.get('priority', 'MEDIUM').upper()]
                task_type = TaskType[dto.get('task_type', 'FEATURE').upper()]
                status = TaskStatus[dto.get('status', 'BACKLOG').upper()]
            except KeyError as e:
                return {'error': f'Invalid enum value: {str(e)}'}, 400

            # Parse dates
            due_date = None
            start_date = None
            if dto.get('due_date'):
                due_date = datetime.fromisoformat(dto.get('due_date').replace('Z', '+00:00'))
            if dto.get('start_date'):
                start_date = datetime.fromisoformat(dto.get('start_date').replace('Z', '+00:00'))

            # Handle labels
            labels = dto.get('labels', [])
            labels_json = json.dumps(labels) if labels else None

            task = Task(
                title=dto.get('title'),
                description=dto.get('description'),
                priority=priority,
                task_type=task_type,
                status=status,
                project_id=project_id,
                sprint_id=dto.get('sprint_id'),
                due_date=due_date,
                start_date=start_date,
                estimated_hours=dto.get('estimated_hours'),
                story_points=dto.get('story_points'),
                acceptance_criteria=dto.get('acceptance_criteria'),
                parent_task_id=dto.get('parent_task_id'),
                labels=labels_json,
                created_by_id=user.id,
                assigned_to_id=dto.get('assigned_to_id')
            )

            db.session.add(task)
            db.session.commit()

            # Create notification for assignee
            if task.assigned_to_id and task.assigned_to_id != user_id:
                Notification.create_notification(
                    user_id=task.assigned_to_id,
                    notification_type=NotificationType.TASK_ASSIGNED,
                    title=f"New Task Assigned: {task.title}",
                    message=f"{user.name} assigned you a new {task.task_type.value.lower()} task",
                    task_id=task.id,
                    related_user_id=user_id,
                    project_id=project_id
                )

            return task.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            return {'error': f'Error creating task: {str(e)}'}, 500

    @staticmethod
    def update_task(task_id, dto, user_id):
        """Update task with enhanced features."""
        try:
            task = Task.query.get_or_404(task_id)
            user = User.query.get_or_404(user_id)

            # Check permissions
            if task.project_id:
                if not user.has_project_permission(task.project_id, 'edit_tasks') and task.project.owner_id != user_id and task.created_by_id != user_id:
                    return {'error': 'Insufficient permissions to update this task'}, 403

            old_assignee_id = task.assigned_to_id
            old_status = task.status

            # Update basic fields
            if 'title' in dto:
                task.title = dto['title']
            if 'description' in dto:
                task.description = dto['description']
            if 'acceptance_criteria' in dto:
                task.acceptance_criteria = dto['acceptance_criteria']

            # Update enums
            if 'priority' in dto:
                try:
                    task.priority = TaskPriority[dto['priority'].upper()]
                except KeyError:
                    return {'error': 'Invalid priority'}, 400

            if 'task_type' in dto:
                try:
                    task.task_type = TaskType[dto['task_type'].upper()]
                except KeyError:
                    return {'error': 'Invalid task type'}, 400

            if 'status' in dto:
                try:
                    new_status = TaskStatus[dto['status'].upper()]
                    task.status = new_status
                    
                    # Set completion date if task is marked as done
                    if new_status == TaskStatus.DONE and old_status != TaskStatus.DONE:
                        task.completion_date = datetime.utcnow()
                    elif new_status != TaskStatus.DONE:
                        task.completion_date = None
                        
                except KeyError:
                    return {'error': 'Invalid status'}, 400

            # Update dates
            if 'due_date' in dto:
                if dto['due_date']:
                    task.due_date = datetime.fromisoformat(dto['due_date'].replace('Z', '+00:00'))
                else:
                    task.due_date = None

            if 'start_date' in dto:
                if dto['start_date']:
                    task.start_date = datetime.fromisoformat(dto['start_date'].replace('Z', '+00:00'))
                else:
                    task.start_date = None

            # Update estimation fields
            if 'estimated_hours' in dto:
                task.estimated_hours = dto['estimated_hours']
            if 'story_points' in dto:
                task.story_points = dto['story_points']

            # Update assignment
            if 'assigned_to_id' in dto:
                task.assigned_to_id = dto['assigned_to_id']

            # Update project and sprint
            if 'project_id' in dto:
                task.project_id = dto['project_id']
            if 'sprint_id' in dto:
                task.sprint_id = dto['sprint_id']

            # Update labels
            if 'labels' in dto:
                labels = dto['labels']
                task.labels = json.dumps(labels) if labels else None

            db.session.commit()

            # Handle notifications
            TaskService._handle_task_update_notifications(task, user_id, old_assignee_id, old_status)

            return task.to_dict(), 200

        except Exception as e:
            db.session.rollback()
            return {'error': f'Error updating task: {str(e)}'}, 500

    @staticmethod
    def delete_task(task_id, user_id):
        """Delete a task."""
        try:
            task = Task.query.get_or_404(task_id)
            user = User.query.get_or_404(user_id)

            # Check permissions
            if task.project_id:
                if not user.has_project_permission(task.project_id, 'delete_tasks') and task.project.owner_id != user_id and task.created_by_id != user_id:
                    return {'error': 'Insufficient permissions to delete this task'}, 403

            db.session.delete(task)
            db.session.commit()
            return {"message": "Task deleted successfully", "task_id": task_id}, 200

        except Exception as e:
            db.session.rollback()
            return {'error': f'Error deleting task: {str(e)}'}, 500

    @staticmethod
    def assign_task(task_id, user_id, assigner_id):
        """Assign a task to a user."""
        try:
            task = Task.query.get_or_404(task_id)
            user = User.query.get_or_404(user_id)
            assigner = User.query.get_or_404(assigner_id)

            # Check permissions
            if task.project_id:
                if not assigner.has_project_permission(task.project_id, 'edit_tasks') and task.project.owner_id != assigner_id:
                    return {'error': 'Insufficient permissions to assign this task'}, 403

            old_assignee_id = task.assigned_to_id
            task.assigned_to_id = user_id
            db.session.commit()

            # Notify new assignee
            if user_id != assigner_id:
                Notification.create_notification(
                    user_id=user_id,
                    notification_type=NotificationType.TASK_ASSIGNED,
                    title=f"Task Assigned: {task.title}",
                    message=f"{assigner.name} assigned you to task '{task.title}'",
                    task_id=task.id,
                    related_user_id=assigner_id,
                    project_id=task.project_id
                )

            return task.to_dict(), 200

        except Exception as e:
            db.session.rollback()
            return {'error': f'Error assigning task: {str(e)}'}, 500

    @staticmethod
    def get_task_by_id(task_id, user_id):
        """Get task by ID with permission check."""
        try:
            task = Task.query.get_or_404(task_id)
            user = User.query.get_or_404(user_id)

            # Check permissions
            if task.project_id:
                if not user.has_project_permission(task.project_id, 'create_tasks') and task.project.owner_id != user_id:
                    return {'error': 'Insufficient permissions to view this task'}, 403

            return task.to_dict(include_subtasks=True), 200

        except Exception as e:
            return {'error': f'Error fetching task: {str(e)}'}, 500

    @staticmethod
    def get_tasks_by_filters(user_id, filters=None):
        """Get tasks with advanced filtering."""
        try:
            user = User.query.get_or_404(user_id)
            
            # Start with base query
            query = Task.query

            # Apply filters
            if filters:
                if filters.get('project_id'):
                    project_id = filters['project_id']
                    project = Project.query.get_or_404(project_id)
                    if not user.has_project_permission(project_id, 'create_tasks') and project.owner_id != user_id:
                        return {'error': 'Insufficient permissions to view tasks in this project'}, 403
                    query = query.filter(Task.project_id == project_id)

                if filters.get('sprint_id'):
                    query = query.filter(Task.sprint_id == filters['sprint_id'])

                if filters.get('assigned_to_id'):
                    query = query.filter(Task.assigned_to_id == filters['assigned_to_id'])

                if filters.get('created_by_id'):
                    query = query.filter(Task.created_by_id == filters['created_by_id'])

                if filters.get('status'):
                    try:
                        status = TaskStatus[filters['status'].upper()]
                        query = query.filter(Task.status == status)
                    except KeyError:
                        return {'error': 'Invalid status filter'}, 400

                if filters.get('priority'):
                    try:
                        priority = TaskPriority[filters['priority'].upper()]
                        query = query.filter(Task.priority == priority)
                    except KeyError:
                        return {'error': 'Invalid priority filter'}, 400

                if filters.get('task_type'):
                    try:
                        task_type = TaskType[filters['task_type'].upper()]
                        query = query.filter(Task.task_type == task_type)
                    except KeyError:
                        return {'error': 'Invalid task type filter'}, 400

                if filters.get('overdue'):
                    query = query.filter(Task.due_date < datetime.utcnow(), Task.status != TaskStatus.DONE)

                if filters.get('parent_task_id'):
                    query = query.filter(Task.parent_task_id == filters['parent_task_id'])

            # Default to user's tasks if no project filter
            if not filters or not filters.get('project_id'):
                # Show tasks assigned to user or created by user
                query = query.filter(
                    db.or_(Task.assigned_to_id == user_id, Task.created_by_id == user_id)
                )

            # Order by priority and due date
            query = query.order_by(Task.priority.desc(), Task.due_date.asc())

            tasks = query.all()
            return [task.to_dict() for task in tasks], 200

        except Exception as e:
            return {'error': f'Error fetching tasks: {str(e)}'}, 500

    @staticmethod
    def add_comment(task_id, user_id, comment_text):
        """Add a comment to a task."""
        try:
            task = Task.query.get_or_404(task_id)
            user = User.query.get_or_404(user_id)

            # Check permissions
            if task.project_id:
                if not user.has_project_permission(task.project_id, 'create_tasks') and task.project.owner_id != user_id:
                    return {'error': 'Insufficient permissions to comment on this task'}, 403

            new_comment = TaskComment(task_id=task_id, user_id=user_id, comment=comment_text)
            db.session.add(new_comment)
            db.session.commit()

            # Notify task assignee and creator
            notification_users = set()
            if task.assigned_to_id and task.assigned_to_id != user_id:
                notification_users.add(task.assigned_to_id)
            if task.created_by_id and task.created_by_id != user_id:
                notification_users.add(task.created_by_id)

            for notify_user_id in notification_users:
                Notification.create_notification(
                    user_id=notify_user_id,
                    notification_type=NotificationType.COMMENT_ADDED,
                    title=f"New Comment on: {task.title}",
                    message=f"{user.name} added a comment to task '{task.title}'",
                    task_id=task.id,
                    related_user_id=user_id,
                    project_id=task.project_id
                )

            return {
                "id": new_comment.id,
                "text": new_comment.comment,
                "author": {
                    "id": user.id,
                    "name": user.name
                },
                "createdAt": new_comment.created_at.isoformat()
            }, 201

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def log_time(task_id, user_id, hours, description, work_date=None):
        """Log time spent on a task."""
        try:
            task = Task.query.get_or_404(task_id)
            user = User.query.get_or_404(user_id)

            # Check permissions
            if task.project_id:
                if not user.has_project_permission(task.project_id, 'create_tasks') and task.project.owner_id != user_id:
                    return {'error': 'Insufficient permissions to log time on this task'}, 403

            if not work_date:
                work_date = datetime.utcnow().date()
            else:
                work_date = datetime.fromisoformat(work_date).date()

            time_log = TimeLog(
                task_id=task_id,
                user_id=user_id,
                hours=hours,
                description=description,
                work_date=work_date
            )

            # Validate hours
            time_log.validate_hours()

            db.session.add(time_log)
            
            # Update task actual hours
            task.actual_hours = (task.actual_hours or 0) + hours
            
            db.session.commit()

            return time_log.to_dict(), 201

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error logging time: {str(e)}'}, 500

    @staticmethod
    def get_task_time_logs(task_id, user_id):
        """Get time logs for a task."""
        try:
            task = Task.query.get_or_404(task_id)
            user = User.query.get_or_404(user_id)

            # Check permissions
            if task.project_id:
                if not user.has_project_permission(task.project_id, 'create_tasks') and task.project.owner_id != user_id:
                    return {'error': 'Insufficient permissions to view time logs for this task'}, 403

            time_logs = TimeLog.query.filter_by(task_id=task_id).order_by(TimeLog.work_date.desc()).all()
            return [log.to_dict() for log in time_logs], 200

        except Exception as e:
            return {'error': f'Error fetching time logs: {str(e)}'}, 500

    @staticmethod
    def get_overdue_tasks(user_id):
        """Get overdue tasks for a user."""
        try:
            user = User.query.get_or_404(user_id)
            
            overdue_tasks = Task.query.filter(
                Task.due_date < datetime.utcnow(),
                Task.status != TaskStatus.DONE,
                db.or_(Task.assigned_to_id == user_id, Task.created_by_id == user_id)
            ).order_by(Task.due_date.asc()).all()

            return [task.to_dict() for task in overdue_tasks], 200

        except Exception as e:
            return {'error': f'Error fetching overdue tasks: {str(e)}'}, 500

    @staticmethod
    def _handle_task_update_notifications(task, user_id, old_assignee_id, old_status):
        """Handle notifications for task updates."""
        user = User.query.get(user_id)
        
        # Notify on assignment change
        if task.assigned_to_id != old_assignee_id:
            if task.assigned_to_id and task.assigned_to_id != user_id:
                Notification.create_notification(
                    user_id=task.assigned_to_id,
                    notification_type=NotificationType.TASK_ASSIGNED,
                    title=f"Task Assigned: {task.title}",
                    message=f"{user.name} assigned you to task '{task.title}'",
                    task_id=task.id,
                    related_user_id=user_id,
                    project_id=task.project_id
                )

        # Notify on status change
        if task.status != old_status:
            notification_users = set()
            if task.assigned_to_id and task.assigned_to_id != user_id:
                notification_users.add(task.assigned_to_id)
            if task.created_by_id and task.created_by_id != user_id:
                notification_users.add(task.created_by_id)

            for notify_user_id in notification_users:
                if task.status == TaskStatus.DONE:
                    notification_type = NotificationType.TASK_COMPLETED
                    message = f"{user.name} marked task '{task.title}' as completed"
                else:
                    notification_type = NotificationType.TASK_UPDATED
                    message = f"{user.name} updated task '{task.title}' status to {task.status.value}"

                Notification.create_notification(
                    user_id=notify_user_id,
                    notification_type=notification_type,
                    title=f"Task Updated: {task.title}",
                    message=message,
                    task_id=task.id,
                    related_user_id=user_id,
                    project_id=task.project_id
                )

    @staticmethod
    def get_user_time_logs(user_id, start_date=None, end_date=None, limit=50):
        """Get time logs for a user with optional date filtering."""
        try:
            from app.models.time_log import TimeLog
            user = User.query.get_or_404(user_id)
            
            # Build query
            query = TimeLog.query.filter_by(user_id=user_id)
            
            # Add date filters if provided
            if start_date:
                try:
                    start = datetime.fromisoformat(start_date).date()
                    query = query.filter(TimeLog.work_date >= start)
                except ValueError:
                    return {'error': 'Invalid start_date format. Use YYYY-MM-DD'}, 400
                    
            if end_date:
                try:
                    end = datetime.fromisoformat(end_date).date()
                    query = query.filter(TimeLog.work_date <= end)
                except ValueError:
                    return {'error': 'Invalid end_date format. Use YYYY-MM-DD'}, 400
            
            # Order by date (most recent first) and limit
            time_logs = query.order_by(TimeLog.work_date.desc(), TimeLog.logged_at.desc()).limit(limit).all()
            
            # Calculate totals
            total_hours = sum(log.hours for log in time_logs)
            
            # Group by date for daily breakdown
            daily_breakdown = {}
            for log in time_logs:
                date_str = log.work_date.isoformat()
                if date_str not in daily_breakdown:
                    daily_breakdown[date_str] = {
                        'date': date_str,
                        'total_hours': 0,
                        'logs': []
                    }
                daily_breakdown[date_str]['total_hours'] += log.hours
                daily_breakdown[date_str]['logs'].append(log.to_dict())
            
            return {
                'time_logs': [log.to_dict() for log in time_logs],
                'total_hours': total_hours,
                'total_entries': len(time_logs),
                'daily_breakdown': list(daily_breakdown.values()),
                'user': user.to_dict()
            }, 200

        except Exception as e:
            return {'error': f'Error fetching user time logs: {str(e)}'}, 500