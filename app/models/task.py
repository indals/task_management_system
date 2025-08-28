# app/models/task.py
from app import db
from datetime import datetime
from .enums import TaskStatus, TaskPriority, TaskType, EstimationUnit

# Import logging and caching utilities
from app.utils.logger import get_logger, log_db_query
from app.utils.cache_utils import cache, cached_per_user, invalidate_user_cache, CacheKeys

# Initialize logger for this module
logger = get_logger('tasks')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.BACKLOG)
    priority = db.Column(db.Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM)
    task_type = db.Column(db.Enum(TaskType), nullable=False, default=TaskType.FEATURE)
    
    # User relationships
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    # Project and Sprint relationships
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=True)
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprint.id', ondelete='SET NULL'), nullable=True)
    
    # Time tracking
    due_date = db.Column(db.DateTime)
    start_date = db.Column(db.DateTime)
    completion_date = db.Column(db.DateTime)
    
    # Estimation and tracking
    estimated_hours = db.Column(db.Float)
    actual_hours = db.Column(db.Float, default=0)
    story_points = db.Column(db.Integer)
    estimation_unit = db.Column(db.Enum(EstimationUnit), default=EstimationUnit.HOURS)
    
    # Additional fields
    labels = db.Column(db.Text)  # JSON string of labels
    acceptance_criteria = db.Column(db.Text)
    
    # Dependencies
    parent_task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='SET NULL'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    assignee = db.relationship('User', foreign_keys=[assigned_to_id], back_populates='assigned_tasks')
    creator = db.relationship('User', foreign_keys=[created_by_id], back_populates='created_tasks')
    project = db.relationship('Project', back_populates='tasks')
    sprint = db.relationship('Sprint', back_populates='tasks')
    
    # Self-referential relationship for parent/child tasks
    parent_task = db.relationship('Task', remote_side=[id], backref='subtasks')
    
    # Child relationships
    comments = db.relationship('TaskComment', back_populates='task', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', back_populates='task', cascade='all, delete-orphan')
    attachments = db.relationship('TaskAttachment', back_populates='task', cascade='all, delete-orphan')
    time_logs = db.relationship('TimeLog', back_populates='task', cascade='all, delete-orphan')

    @classmethod
    def create_task(cls, title, description, created_by_id, project_id=None, 
                   status=TaskStatus.BACKLOG, priority=TaskPriority.MEDIUM, 
                   task_type=TaskType.FEATURE, **kwargs):
        """Create a new task with comprehensive logging and cache management."""
        logger.info(f"Creating new task: '{title}' by user {created_by_id}")
        
        try:
            task = cls(
                title=title,
                description=description,
                created_by_id=created_by_id,
                project_id=project_id,
                status=status,
                priority=priority,
                task_type=task_type,
                **kwargs
            )
            
            db.session.add(task)
            db.session.commit()
            
            logger.info(f"Task created successfully: {task.id} - '{title}'")
            
            # Clear relevant caches
            cls._clear_task_caches(project_id=project_id, user_id=created_by_id)
            
            return task
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Task creation failed for '{title}': {str(e)}")
            raise

    def update_task(self, title=None, description=None, status=None, priority=None, 
                   task_type=None, assigned_to_id=None, due_date=None, start_date=None,
                   estimated_hours=None, story_points=None, estimation_unit=None,
                   acceptance_criteria=None, **kwargs):
        """Update task with logging and cache invalidation."""
        logger.info(f"Updating task {self.id}")
        
        # Track changes for logging
        changes = []
        old_assigned_to_id = self.assigned_to_id
        old_status = self.status
        old_project_id = self.project_id
        
        try:
            if title and title != self.title:
                changes.append(f"title: '{self.title}' -> '{title}'")
                self.title = title
            
            if description is not None and description != self.description:
                changes.append("description updated")
                self.description = description
            
            if status and status != self.status:
                changes.append(f"status: {self.status.value} -> {status.value}")
                self.status = status
                
                # Set completion date if task is completed
                if status == TaskStatus.DONE and not self.completion_date:
                    self.completion_date = datetime.utcnow()
                    changes.append("completion_date set")
                elif status != TaskStatus.DONE and self.completion_date:
                    self.completion_date = None
                    changes.append("completion_date cleared")
            
            if priority and priority != self.priority:
                changes.append(f"priority: {self.priority.value} -> {priority.value}")
                self.priority = priority
            
            if task_type and task_type != self.task_type:
                changes.append(f"task_type: {self.task_type.value} -> {task_type.value}")
                self.task_type = task_type
            
            if assigned_to_id != self.assigned_to_id:
                if assigned_to_id is None:
                    changes.append(f"unassigned from user {self.assigned_to_id}")
                elif self.assigned_to_id is None:
                    changes.append(f"assigned to user {assigned_to_id}")
                else:
                    changes.append(f"reassigned from user {self.assigned_to_id} to {assigned_to_id}")
                self.assigned_to_id = assigned_to_id
            
            if due_date != self.due_date:
                changes.append("due_date updated")
                self.due_date = due_date
            
            if start_date != self.start_date:
                changes.append("start_date updated")
                self.start_date = start_date
            
            if estimated_hours is not None and estimated_hours != self.estimated_hours:
                changes.append(f"estimated_hours: {self.estimated_hours} -> {estimated_hours}")
                self.estimated_hours = estimated_hours
            
            if story_points is not None and story_points != self.story_points:
                changes.append(f"story_points: {self.story_points} -> {story_points}")
                self.story_points = story_points
            
            if estimation_unit and estimation_unit != self.estimation_unit:
                changes.append(f"estimation_unit: {estimation_unit.value}")
                self.estimation_unit = estimation_unit
            
            if acceptance_criteria is not None and acceptance_criteria != self.acceptance_criteria:
                changes.append("acceptance_criteria updated")
                self.acceptance_criteria = acceptance_criteria
            
            if changes:
                db.session.commit()
                logger.info(f"Task {self.id} updated: {', '.join(changes)}")
                
                # Clear relevant caches
                users_to_invalidate = [old_assigned_to_id, self.assigned_to_id, self.created_by_id]
                self._invalidate_task_caches(users_to_invalidate, old_project_id)
                
            else:
                logger.debug(f"No changes in task update for task {self.id}")
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"Task update failed for task {self.id}: {str(e)}")
            raise

    def assign_to_user(self, user_id):
        """Assign task to a user with logging and cache management."""
        if self.assigned_to_id == user_id:
            logger.debug(f"Task {self.id} already assigned to user {user_id}")
            return
            
        old_assigned_to_id = self.assigned_to_id
        
        try:
            self.assigned_to_id = user_id
            db.session.commit()
            
            if old_assigned_to_id:
                logger.info(f"Task {self.id} reassigned from user {old_assigned_to_id} to {user_id}")
            else:
                logger.info(f"Task {self.id} assigned to user {user_id}")
            
            # Invalidate caches for both old and new assignees
            if old_assigned_to_id:
                invalidate_user_cache(old_assigned_to_id, CacheKeys.USER_TASKS)
            if user_id:
                invalidate_user_cache(user_id, CacheKeys.USER_TASKS)
            
            # Clear project and sprint task caches
            self._clear_project_caches()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Task assignment failed for task {self.id}: {str(e)}")
            raise

    def unassign(self):
        """Unassign task with logging and cache management."""
        if not self.assigned_to_id:
            logger.debug(f"Task {self.id} is not assigned to anyone")
            return
            
        old_assigned_to_id = self.assigned_to_id
        
        try:
            self.assigned_to_id = None
            db.session.commit()
            
            logger.info(f"Task {self.id} unassigned from user {old_assigned_to_id}")
            
            # Invalidate old assignee's cache
            invalidate_user_cache(old_assigned_to_id, CacheKeys.USER_TASKS)
            self._clear_project_caches()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Task unassignment failed for task {self.id}: {str(e)}")
            raise

    def move_to_project(self, project_id):
        """Move task to different project with logging and cache management."""
        if self.project_id == project_id:
            logger.debug(f"Task {self.id} already in project {project_id}")
            return
            
        old_project_id = self.project_id
        
        try:
            self.project_id = project_id
            db.session.commit()
            
            logger.info(f"Task {self.id} moved from project {old_project_id} to {project_id}")
            
            # Clear caches for both old and new projects
            self._clear_task_caches(project_id=old_project_id)
            self._clear_task_caches(project_id=project_id)
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Task project move failed for task {self.id}: {str(e)}")
            raise

    def move_to_sprint(self, sprint_id):
        """Move task to different sprint with logging and cache management."""
        if self.sprint_id == sprint_id:
            logger.debug(f"Task {self.id} already in sprint {sprint_id}")
            return
            
        old_sprint_id = self.sprint_id
        
        try:
            self.sprint_id = sprint_id
            db.session.commit()
            
            logger.info(f"Task {self.id} moved from sprint {old_sprint_id} to {sprint_id}")
            
            # Clear sprint caches
            if old_sprint_id:
                cache.delete(f"sprint_{old_sprint_id}_tasks")
            if sprint_id:
                cache.delete(f"sprint_{sprint_id}_tasks")
            
            self._clear_project_caches()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Task sprint move failed for task {self.id}: {str(e)}")
            raise

    @cache.memoize(timeout=300)
    def get_progress_percentage(self):
        """Calculate task progress based on subtasks or time logged with caching."""
        logger.debug(f"Calculating progress for task {self.id}")
        
        if self.subtasks:
            completed_subtasks = sum(1 for subtask in self.subtasks if subtask.status == TaskStatus.DONE)
            progress = (completed_subtasks / len(self.subtasks)) * 100 if self.subtasks else 0
        elif self.estimated_hours and self.actual_hours:
            progress = min((self.actual_hours / self.estimated_hours) * 100, 100)
        else:
            progress = 0 if self.status != TaskStatus.DONE else 100
            
        logger.debug(f"Task {self.id} progress: {progress:.1f}%")
        return progress

    def is_overdue(self):
        """Check if task is overdue."""
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and self.status not in [TaskStatus.DONE, TaskStatus.CANCELLED]

    @cache.memoize(timeout=600)
    def get_time_spent(self):
        """Get total time spent on this task with caching."""
        logger.debug(f"Calculating time spent for task {self.id}")
        total_time = sum(log.hours for log in self.time_logs)
        logger.debug(f"Task {self.id} total time: {total_time} hours")
        return total_time

    def add_label(self, label):
        """Add a label to the task with logging and cache invalidation."""
        import json
        labels = []
        if self.labels:
            try:
                labels = json.loads(self.labels)
            except json.JSONDecodeError:
                labels = []
        
        if label not in labels:
            labels.append(label)
            self.labels = json.dumps(labels)
            
            try:
                db.session.commit()
                logger.info(f"Added label '{label}' to task {self.id}")
                self._invalidate_task_detail_cache()
            except Exception as e:
                db.session.rollback()
                logger.error(f"Failed to add label '{label}' to task {self.id}: {str(e)}")
                raise

    def remove_label(self, label):
        """Remove a label from the task with logging and cache invalidation."""
        import json
        labels = []
        if self.labels:
            try:
                labels = json.loads(self.labels)
            except json.JSONDecodeError:
                return
        
        if label in labels:
            labels.remove(label)
            self.labels = json.dumps(labels)
            
            try:
                db.session.commit()
                logger.info(f"Removed label '{label}' from task {self.id}")
                self._invalidate_task_detail_cache()
            except Exception as e:
                db.session.rollback()
                logger.error(f"Failed to remove label '{label}' from task {self.id}: {str(e)}")
                raise

    def add_time_log(self, hours, description=None, user_id=None):
        """Add time log entry with logging and cache invalidation."""
        from .time_log import TimeLog
        
        try:
            time_log = TimeLog(
                task_id=self.id,
                user_id=user_id or self.assigned_to_id,
                hours=hours,
                description=description
            )
            
            # Update actual hours
            self.actual_hours = (self.actual_hours or 0) + hours
            
            db.session.add(time_log)
            db.session.commit()
            
            logger.info(f"Added {hours} hours time log to task {self.id}")
            
            # Invalidate relevant caches
            self._invalidate_task_detail_cache()
            cache.delete(f"task_{self.id}_time_spent")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to add time log to task {self.id}: {str(e)}")
            raise

    def delete_task(self):
        """Delete task with comprehensive logging and cache cleanup."""
        logger.info(f"Deleting task {self.id}: '{self.title}'")
        
        # Store info before deletion for cache cleanup
        project_id = self.project_id
        sprint_id = self.sprint_id
        assigned_to_id = self.assigned_to_id
        created_by_id = self.created_by_id
        
        try:
            db.session.delete(self)
            db.session.commit()
            
            logger.info(f"Task {self.id} deleted successfully")
            
            # Clear all related caches
            users_to_invalidate = [assigned_to_id, created_by_id]
            self._clear_task_caches(
                project_id=project_id, 
                sprint_id=sprint_id, 
                users=users_to_invalidate
            )
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Task deletion failed for task {self.id}: {str(e)}")
            raise

    @classmethod
    @cache.cached(timeout=300, key_prefix='project_tasks')
    def get_project_tasks(cls, project_id, status=None):
        """Get tasks for a project with caching."""
        logger.debug(f"Fetching tasks for project {project_id}")
        
        query = cls.query.filter_by(project_id=project_id)
        if status:
            query = query.filter_by(status=status)
        
        tasks = query.all()
        logger.debug(f"Found {len(tasks)} tasks for project {project_id}")
        return tasks

    @classmethod
    @cache.cached(timeout=300, key_prefix='sprint_tasks')
    def get_sprint_tasks(cls, sprint_id):
        """Get tasks for a sprint with caching."""
        logger.debug(f"Fetching tasks for sprint {sprint_id}")
        
        tasks = cls.query.filter_by(sprint_id=sprint_id).all()
        logger.debug(f"Found {len(tasks)} tasks for sprint {sprint_id}")
        return tasks

    @classmethod
    def get_overdue_tasks(cls):
        """Get all overdue tasks with logging."""
        logger.debug("Fetching overdue tasks")
        
        now = datetime.utcnow()
        overdue_tasks = cls.query.filter(
            cls.due_date < now,
            cls.status.notin_([TaskStatus.DONE, TaskStatus.CANCELLED])
        ).all()
        
        logger.info(f"Found {len(overdue_tasks)} overdue tasks")
        return overdue_tasks

    def to_dict(self, include_subtasks=False):
        """Convert task to dictionary with caching consideration."""
        import json
        
        # Parse labels from JSON string
        labels_list = []
        if self.labels:
            try:
                labels_list = json.loads(self.labels)
            except json.JSONDecodeError:
                labels_list = []

        result = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'priority': self.priority.value,
            'task_type': self.task_type.value,
            'assigned_to': self.assignee.to_dict() if self.assignee else None,
            'created_by': self.creator.to_dict() if self.creator else None,
            'project': self.project.to_dict() if self.project else None,
            'sprint': self.sprint.to_dict() if self.sprint else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'estimated_hours': self.estimated_hours,
            'actual_hours': self.actual_hours,
            'story_points': self.story_points,
            'estimation_unit': self.estimation_unit.value if self.estimation_unit else None,
            'labels': labels_list,
            'acceptance_criteria': self.acceptance_criteria,
            'parent_task_id': self.parent_task_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'comments_count': len(self.comments),
            'attachments_count': len(self.attachments),
            'time_logs_count': len(self.time_logs),
            'progress_percentage': self.get_progress_percentage(),
            'is_overdue': self.is_overdue()
        }
        
        if include_subtasks:
            result['subtasks'] = [subtask.to_dict() for subtask in self.subtasks]
            
        return result

    # Private helper methods for cache management
    def _invalidate_task_detail_cache(self):
        """Invalidate task detail caches."""
        cache.delete(f"task_{self.id}_progress")
        cache.delete(f"task_{self.id}_time_spent")

    def _invalidate_task_caches(self, users_to_invalidate=None, old_project_id=None):
        """Invalidate task-related caches."""
        # Invalidate user caches
        if users_to_invalidate:
            for user_id in filter(None, users_to_invalidate):
                invalidate_user_cache(user_id, CacheKeys.USER_TASKS)
        
        # Invalidate project caches
        if old_project_id:
            cache.delete(f"project_{old_project_id}_tasks")
        if self.project_id:
            cache.delete(f"project_{self.project_id}_tasks")
        
        # Invalidate sprint caches
        if self.sprint_id:
            cache.delete(f"sprint_{self.sprint_id}_tasks")
        
        self._invalidate_task_detail_cache()

    def _clear_project_caches(self):
        """Clear project-related caches."""
        if self.project_id:
            cache.delete(f"project_{self.project_id}_tasks")
            invalidate_user_cache(self.created_by_id, CacheKeys.USER_PROJECTS)
            if self.assigned_to_id:
                invalidate_user_cache(self.assigned_to_id, CacheKeys.USER_PROJECTS)

    @classmethod
    def _clear_task_caches(cls, project_id=None, sprint_id=None, user_id=None, users=None):
        """Clear task-related caches."""
        if project_id:
            cache.delete(f"project_{project_id}_tasks")
        if sprint_id:
            cache.delete(f"sprint_{sprint_id}_tasks")
        if user_id:
            invalidate_user_cache(user_id, CacheKeys.USER_TASKS)
        if users:
            for uid in filter(None, users):
                invalidate_user_cache(uid, CacheKeys.USER_TASKS)