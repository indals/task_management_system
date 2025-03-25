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

    # @staticmethod
    # def get_task_completion_rate(user_id, time_period):
    #     query = Task.query.filter_by(assignee_id=user_id)  # Filter tasks for the user
    #     # Apply filtering based on `time_period` logic (week, month, year)
    #     # Compute completion rate and return stats

    @staticmethod
    def get_task_completion_rate(user_id, time_period='month'):
        """Returns task completion rate for a specific time period."""
        from datetime import datetime, timedelta

        # Calculate the date range based on time_period
        now = datetime.utcnow()
        if time_period == 'week':
            start_date = now - timedelta(days=7)
        elif time_period == 'month':
            start_date = now - timedelta(days=30)
        elif time_period == 'year':
            start_date = now - timedelta(days=365)
        else:
            return {'error': 'Invalid time period. Choose week, month, or year'}, 400

        # Get all tasks for the user in the time period
        total_tasks = Task.query.filter(
            Task.assigned_to_id == user_id,
            Task.created_at >= start_date
        ).count()

        # Get completed tasks
        completed_tasks = Task.query.filter(
            Task.assigned_to_id == user_id,
            Task.status == TaskStatus.COMPLETED,
            Task.created_at >= start_date
        ).count()

        # Calculate completion rate
        completion_rate = (completed_tasks / total_tasks) if total_tasks > 0 else 0

        return {
            'time_period': time_period,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': completion_rate,
            'start_date': start_date.isoformat(),
            'end_date': now.isoformat()
        }