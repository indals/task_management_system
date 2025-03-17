from app.models.task import Task
from app.models.user import User
from datetime import datetime
from app.models.enums import TaskStatus
from sqlalchemy.sql import func

class AnalyticsService:

    @staticmethod
    def get_user_performance(user_id):
        """Returns task completion statistics for a specific user."""
        user = User.query.get_or_404(user_id)

        total_tasks = Task.query.filter_by(assigned_to_id=user.id).count()
        completed_tasks = Task.query.filter_by(
            assigned_to_id=user.id,
            status=TaskStatus.COMPLETED.value
        ).count()

        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': (completed_tasks / total_tasks) if total_tasks > 0 else 0
        }

    @staticmethod
    def get_team_productivity():
        """Returns the productivity stats for all users in the system."""
        users = User.query.all()
        team_stats = [
            {
                'user': user.to_dict(),
                'performance': AnalyticsService.get_user_performance(user.id)
            }
            for user in users
        ]
        return team_stats

    @staticmethod
    def get_overdue_tasks():
        """Retrieves all tasks that are overdue but not yet completed."""
        tasks = Task.query.filter(
            Task.due_date.isnot(None),  # Ensure due_date is not None
            Task.due_date < datetime.utcnow(),
            Task.status != TaskStatus.COMPLETED.value
        ).all()
        return [task.to_dict() for task in tasks]

    @staticmethod
    def get_task_completion_rate(user_id, time_period):
        query = Task.query.filter_by(assignee_id=user_id)  # Filter tasks for the user
        # Apply filtering based on `time_period` logic (week, month, year)
        # Compute completion rate and return stats

