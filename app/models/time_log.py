# app/models/time_log.py
from app import db
from datetime import datetime, date, timedelta

# Import logging and caching utilities
from app.utils.logger import get_logger, log_db_query
from app.utils.cache_utils import cache, cached_per_user, invalidate_user_cache, CacheKeys

# Initialize logger for this module
logger = get_logger('time_logs')

class TimeLog(db.Model):
    __tablename__ = 'time_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    # Time tracking
    hours = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    
    # Date tracking
    work_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    
    # Timestamps
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    task = db.relationship('Task', back_populates='time_logs')
    user = db.relationship('User', backref='time_logs')

    def __init__(self, **kwargs):
        """Initialize TimeLog with validation and logging."""
        super().__init__(**kwargs)
        logger.debug(f"Creating new TimeLog for user {self.user_id}, task {self.task_id}")

    def to_dict(self):
        """Convert TimeLog to dictionary."""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'user_id': self.user_id,
            'hours': self.hours,
            'description': self.description,
            'work_date': self.work_date.isoformat(),
            'logged_at': self.logged_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'task': self.task.to_dict() if self.task else None,
            'user': self.user.to_dict() if self.user else None,
            'hours_formatted': self.get_formatted_hours()
        }

    def get_formatted_hours(self):
        """Return formatted hours (e.g., '2h 30m')."""
        if not self.hours:
            return "0h"
        
        total_minutes = int(self.hours * 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        if hours > 0 and minutes > 0:
            return f"{hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h"
        else:
            return f"{minutes}m"

    def save(self):
        """Save time log with validation, logging, and cache invalidation."""
        try:
            # Validate before saving
            self.validate_hours()
            
            is_new = self.id is None
            
            db.session.add(self)
            db.session.commit()
            
            # Log the operation
            operation = "created" if is_new else "updated"
            logger.info(f"TimeLog {operation}: {self.hours}h for task {self.task_id} by user {self.user_id} on {self.work_date}")
            
            # Invalidate relevant caches
            self._invalidate_caches()
            
            return self
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to save TimeLog for user {self.user_id}, task {self.task_id}: {str(e)}")
            raise

    def delete(self):
        """Delete time log with logging and cache invalidation."""
        user_id = self.user_id
        task_id = self.task_id
        hours = self.hours
        
        try:
            db.session.delete(self)
            db.session.commit()
            
            logger.info(f"TimeLog deleted: {hours}h for task {task_id} by user {user_id}")
            
            # Invalidate caches for this user and task
            invalidate_user_cache(user_id, "time_logs")
            cache.delete(f"task_total_hours_{task_id}")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to delete TimeLog {self.id}: {str(e)}")
            raise

    def _invalidate_caches(self):
        """Invalidate all related caches."""
        # User-specific caches
        invalidate_user_cache(self.user_id, "time_logs")
        invalidate_user_cache(self.user_id, "daily_hours")
        invalidate_user_cache(self.user_id, "weekly_hours")
        
        # Task-specific caches
        cache.delete(f"task_total_hours_{self.task_id}")
        
        # Date-specific caches
        cache.delete(f"daily_hours_{self.user_id}_{self.work_date}")

    @classmethod
    @cache.cached(timeout=300)
    def get_user_daily_hours(cls, user_id, date):
        """Get total hours logged by user on a specific date with caching."""
        cache_key = f"daily_hours_{user_id}_{date}"
        
        logger.debug(f"Fetching daily hours for user {user_id} on {date}")
        
        logs = cls.query.filter_by(user_id=user_id, work_date=date).all()
        total_hours = sum(log.hours for log in logs)
        
        logger.debug(f"User {user_id} logged {total_hours}h on {date}")
        return total_hours

    @classmethod
    @cache.cached(timeout=600)
    def get_task_total_hours(cls, task_id):
        """Get total hours logged for a specific task with caching."""
        logger.debug(f"Fetching total hours for task {task_id}")
        
        logs = cls.query.filter_by(task_id=task_id).all()
        total_hours = sum(log.hours for log in logs)
        
        logger.debug(f"Task {task_id} has {total_hours}h logged")
        return total_hours

    @classmethod
    @cache.cached(timeout=300)
    def get_user_weekly_hours(cls, user_id, start_date, end_date):
        """Get total hours logged by user in a date range with caching."""
        cache_key = f"weekly_hours_{user_id}_{start_date}_{end_date}"
        
        logger.debug(f"Fetching weekly hours for user {user_id} from {start_date} to {end_date}")
        
        logs = cls.query.filter(
            cls.user_id == user_id,
            cls.work_date >= start_date,
            cls.work_date <= end_date
        ).all()
        
        total_hours = sum(log.hours for log in logs)
        logger.debug(f"User {user_id} logged {total_hours}h between {start_date} and {end_date}")
        return total_hours

    @classmethod
    def get_user_monthly_hours(cls, user_id, year, month):
        """Get total hours logged by user in a specific month."""
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        return cls.get_user_weekly_hours(user_id, start_date, end_date)

    @classmethod
    @cached_per_user(timeout=300, key_prefix="user_recent_logs")
    def get_user_recent_logs(cls, user_id, days=7):
        """Get recent time logs for a user with caching."""
        start_date = datetime.utcnow().date() - timedelta(days=days)
        
        logger.debug(f"Fetching recent {days} days of logs for user {user_id}")
        
        logs = cls.query.filter(
            cls.user_id == user_id,
            cls.work_date >= start_date
        ).order_by(cls.work_date.desc(), cls.logged_at.desc()).all()
        
        return logs

    @classmethod
    def get_productivity_stats(cls, user_id, days=30):
        """Get productivity statistics for a user."""
        start_date = datetime.utcnow().date() - timedelta(days=days)
        
        logs = cls.query.filter(
            cls.user_id == user_id,
            cls.work_date >= start_date
        ).all()
        
        if not logs:
            return {
                'total_hours': 0,
                'avg_daily_hours': 0,
                'productive_days': 0,
                'total_days': days
            }
        
        total_hours = sum(log.hours for log in logs)
        unique_days = len(set(log.work_date for log in logs))
        avg_daily = total_hours / unique_days if unique_days > 0 else 0
        
        stats = {
            'total_hours': total_hours,
            'avg_daily_hours': round(avg_daily, 2),
            'productive_days': unique_days,
            'total_days': days
        }
        
        logger.debug(f"Productivity stats for user {user_id}: {stats}")
        return stats

    def validate_hours(self):
        """Validate that hours are reasonable with enhanced logging."""
        logger.debug(f"Validating {self.hours}h for user {self.user_id} on {self.work_date}")
        
        if self.hours < 0:
            logger.warning(f"Negative hours rejected: {self.hours}h for user {self.user_id}")
            raise ValueError("Hours cannot be negative")
            
        if self.hours > 24:
            logger.warning(f"Excessive hours rejected: {self.hours}h for user {self.user_id}")
            raise ValueError("Hours cannot exceed 24 per day")
        
        # Check if total daily hours for user would exceed reasonable limit
        existing_total = TimeLog.get_user_daily_hours(self.user_id, self.work_date)
        
        # If updating existing log, subtract its current hours from the total
        if self.id:
            original_log = TimeLog.query.get(self.id)
            if original_log:
                existing_total -= original_log.hours
        
        if existing_total + self.hours > 24:
            logger.warning(f"Daily limit exceeded: {existing_total + self.hours}h total for user {self.user_id} on {self.work_date}")
            raise ValueError(f"Total daily hours would exceed 24 hours (current: {existing_total:.1f}h)")

    @classmethod
    def bulk_create(cls, time_logs_data):
        """Create multiple time logs efficiently with proper logging."""
        logger.info(f"Bulk creating {len(time_logs_data)} time logs")
        
        try:
            created_logs = []
            for log_data in time_logs_data:
                time_log = cls(**log_data)
                time_log.validate_hours()
                db.session.add(time_log)
                created_logs.append(time_log)
            
            db.session.commit()
            
            # Invalidate relevant caches for all affected users
            affected_users = set(log.user_id for log in created_logs)
            for user_id in affected_users:
                invalidate_user_cache(user_id, "time_logs")
            
            logger.info(f"Successfully created {len(created_logs)} time logs")
            return created_logs
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Bulk create failed: {str(e)}")
            raise

    def update_hours(self, new_hours, description=None):
        """Update time log hours with validation and logging."""
        old_hours = self.hours
        self.hours = new_hours
        
        if description is not None:
            self.description = description
        
        try:
            self.validate_hours()
            db.session.commit()
            
            logger.info(f"TimeLog {self.id} updated: {old_hours}h -> {new_hours}h for user {self.user_id}")
            self._invalidate_caches()
            
        except Exception as e:
            db.session.rollback()
            self.hours = old_hours  # Restore original value
            logger.error(f"Failed to update TimeLog {self.id}: {str(e)}")
            raise