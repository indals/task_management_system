from app.models.task import Task
from app.models.task_comment import TaskComment
from app.models.user import User
from app import db
from app.models.enums import TaskStatus, TaskPriority


class TaskService:
    @staticmethod
    def create_task(dto, user_id, assigned_to_id = None):
        user = User.query.get_or_404(user_id)

        # Convert priority to enum
        try:
            priority = TaskPriority[dto.get('priority', 'MEDIUM').upper()]
        except KeyError:
            return {'error': 'Invalid priority'}

        task = Task(
            title=dto.get('title'),
            description=dto.get('description'),
            priority=priority,
            due_date=dto.get('due_date'),
            created_by_id=user.id,
            status=TaskStatus.PENDING,
            assigned_to_id=assigned_to_id
        )

        db.session.add(task)
        db.session.commit()
        return task.to_dict()

    @staticmethod
    def update_task(task_id, dto):
        task = Task.query.get_or_404(task_id)

        if 'title' in dto:
            task.title = dto.get('title')

        if 'description' in dto:
            task.description = dto.get('description')

        if 'priority' in dto:
            try:
                task.priority = TaskPriority[dto.get('priority').upper()]
            except KeyError:
                return {'error': 'Invalid priority'}

        if 'status' in dto:
            try:
                task.status = TaskStatus[dto.get('status').upper()]
            except KeyError:
                return {'error': 'Invalid status'}

        if 'due_date' in dto:
            task.due_date = dto.get('due_date')

        db.session.commit()
        return task.to_dict()

    @staticmethod
    def delete_task(task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted successfully", "task_id": task_id}

    @staticmethod
    def assign_task(task_id, user_id):
        task = Task.query.get_or_404(task_id)
        user = User.query.get_or_404(user_id)
        task.assigned_to_id = user.id
        db.session.commit()
        return task.to_dict()

    @staticmethod
    def get_task_by_id(task_id):
        task = Task.query.get_or_404(task_id)
        return task.to_dict()

    @staticmethod
    def get_tasks_by_user(user_id):
        if not user_id:
            print("No user ID provided!")
            return []

        try:
            user_id = int(user_id)  # Ensure it's an integer
        except ValueError:
            print(f"Invalid user ID: {user_id}")
            return []

        try:
            tasks = Task.query.filter_by(assigned_to_id=user_id).all()
            print(f"Tasks found: {tasks}")  # Debugging: Log fetched tasks

            if not tasks:
                print("No tasks found for the user.")

            return [task.to_dict() for task in tasks]

        except Exception as e:
            print(f"Database Error: {e}")  # Catch and log any DB errors
            return []

        tasks = Task.query.filter_by(assigned_to_id=user_id).all()
        return [task.to_dict() for task in tasks]

    @staticmethod
    def get_tasks_by_status(status):
        if not status:
            return Task.query.all()

        try:
            status_enum = TaskStatus[status.upper()]
            tasks = Task.query.filter_by(status=status_enum).all()
            return [task.to_dict() for task in tasks]
        except KeyError:
            return {'error': 'Invalid status'}

    @staticmethod
    def get_tasks_created_by_user(user_id):
        """
        Fetch all tasks created by a manager.
        """
        if not user_id:
            return []

        try:
            user_id = int(user_id)
        except ValueError:
            return []

        tasks = Task.query.filter_by(created_by_id=user_id).all()
        return [task.to_dict() for task in tasks]

    @staticmethod
    def add_comment(task_id, user_id, comment_text):
        try:
            new_comment = TaskComment(task_id=task_id, user_id=user_id, comment=comment_text)
            db.session.add(new_comment)
            db.session.commit()

            # Fetch the author
            author = User.query.get(user_id)

            return {
                "id": new_comment.id,
                "text": new_comment.comment,
                "author": {
                    "id": author.id,
                    "name": author.name
                },
                "createdAt": new_comment.created_at.isoformat()
            }
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}