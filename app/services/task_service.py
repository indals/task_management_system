from app.models.task import Task
from app.models.user import User
from app import db
from app.models.enums import TaskStatus, TaskPriority


class TaskService:
    @staticmethod
    def create_task(dto, user_id):
        user = User.query.get_or_404(user_id)
        task = Task(
            title=dto.get('title'),
            description=dto.get('description'),
            priority=TaskPriority[dto.get('priority').upper()],
            due_date=dto.get('due_date') if 'due_date' in dto else None,  # Handling due_date
            created_by_id=user.id  # Correcting user_id assignment
        )
        db.session.add(task)
        db.session.commit()
        return task.to_dict()

    @staticmethod
    def update_task(task_id, dto):
        task = Task.query.get_or_404(task_id)
        task.title = dto.title
        task.description = dto.description
        task.priority = dto.priority
        task.status = dto.status
        task.due_date = dto.due_date if hasattr(dto, 'due_date') else task.due_date  # Update due_date if provided
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
        task.assigned_to_id = user.id  # Corrected assignment
        db.session.commit()
        return task.to_dict()

    @staticmethod
    def get_task_by_id(task_id):
        task = Task.query.get_or_404(task_id)
        return task.to_dict()

    @staticmethod
    def get_tasks_by_user(user_id):
        tasks = Task.query.filter_by(assigned_to_id=user_id).all()
        return [task.to_dict() for task in tasks]

    @staticmethod
    def get_tasks_by_status(status):
        if isinstance(status, str):
            try:
                status = TaskStatus[status.upper()]  # Convert string to Enum
            except KeyError:
                return {"error": "Invalid status"}, 400

        tasks = Task.query.filter_by(status=status).all()
        return [task.to_dict() for task in tasks]
