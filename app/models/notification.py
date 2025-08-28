# app/models/notification.py
from app import db
from datetime import datetime, timedelta
from .enums import NotificationType

# Import logging and caching utilities
from app.utils.logger import get_logger, log_db_query
from app.utils.cache_utils import cache, cached_per_user, invalidate_user_cache, CacheKeys

# Initialize logger for this module
logger = get_logger('notifications')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'), nullable=True)
    
    # Notification details
    type = db.Column(db.Enum(NotificationType), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    # Additional context
    related_user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)  # User who triggered the notification
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=True)
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprint.id', ondelete='CASCADE'), nullable=True)
    
    # Status
    read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='notifications', foreign_keys=[user_id])
    task = db.relationship('Task', back_populates='notifications')
    related_user = db.relationship('User', foreign_keys=[related_user_id])
    project = db.relationship('Project')
    sprint = db.relationship('Sprint')

    def mark_as_read(self):
        """Mark notification as read with logging and cache invalidation."""
        if not self.read:
            logger.info(f"Marking notification {self.id} as read for user {self.user_id}")
            self.read = True
            self.read_at = datetime.utcnow()
            
            try:
                db.session.commit()
                log_db_query("UPDATE", "notifications", self.id, f"marked_as_read")
                
                # Invalidate user's notification caches
                invalidate_user_cache(self.user_id, CacheKeys.USER_NOTIFICATIONS)
                cache.delete(f'user_unread_count_{self.user_id}')
                
                logger.debug(f"Successfully marked notification {self.id} as read")
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Failed to mark notification {self.id} as read: {str(e)}")
                raise
        else:
            logger.debug(f"Notification {self.id} already marked as read")

    def mark_as_unread(self):
        """Mark notification as unread with logging and cache invalidation."""
        if self.read:
            logger.info(f"Marking notification {self.id} as unread for user {self.user_id}")
            self.read = False
            self.read_at = None
            
            try:
                db.session.commit()
                log_db_query("UPDATE", "notifications", self.id, f"marked_as_unread")
                
                # Invalidate user's notification caches
                invalidate_user_cache(self.user_id, CacheKeys.USER_NOTIFICATIONS)
                cache.delete(f'user_unread_count_{self.user_id}')
                
                logger.debug(f"Successfully marked notification {self.id} as unread")
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Failed to mark notification {self.id} as unread: {str(e)}")
                raise
        else:
            logger.debug(f"Notification {self.id} already marked as unread")

    @classmethod
    def create_notification(cls, user_id, notification_type, title, message, 
                          task_id=None, related_user_id=None, project_id=None, sprint_id=None):
        """Create a new notification with comprehensive logging and cache management."""
        logger.info(f"Creating notification: {notification_type.value} for user {user_id}")
        logger.debug(f"Notification details - Title: '{title}', Task: {task_id}, Project: {project_id}")
        
        notification = cls(
            user_id=user_id,
            task_id=task_id,
            type=notification_type,
            title=title,
            message=message,
            related_user_id=related_user_id,
            project_id=project_id,
            sprint_id=sprint_id
        )
        
        try:
            db.session.add(notification)
            db.session.commit()
            
            logger.info(f"Successfully created notification {notification.id} for user {user_id}")
            log_db_query("INSERT", "notifications", notification.id)
            
            # Invalidate user's notification caches
            invalidate_user_cache(user_id, CacheKeys.USER_NOTIFICATIONS)
            cache.delete(f'user_unread_count_{user_id}')
            cache.delete(f'user_recent_notifications_{user_id}')
            
            # Try to broadcast via socket
            try:
                from app.utils.socket_utils import broadcast_notification
                broadcast_notification(user_id, notification.to_dict())
                logger.debug(f"Socket broadcast successful for notification {notification.id}")
            except Exception as socket_e:
                logger.warning(f"Socket broadcast failed for notification {notification.id}: {str(socket_e)}")
            
            return notification
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to create notification for user {user_id}: {str(e)}")
            raise

    @classmethod
    @cache.cached(timeout=120, key_prefix='user_unread_count')
    def get_unread_count(cls, user_id):
        """Get count of unread notifications for a user with caching."""
        logger.debug(f"Fetching unread notification count for user {user_id}")
        count = cls.query.filter_by(user_id=user_id, read=False).count()
        log_db_query("SELECT", "notifications", None, f"unread_count_user_{user_id}")
        logger.debug(f"User {user_id} has {count} unread notifications")
        return count

    @classmethod
    @cached_per_user(timeout=300, key_prefix=CacheKeys.USER_NOTIFICATIONS)
    def get_user_notifications(cls, user_id, limit=50, offset=0, unread_only=False):
        """Get user notifications with caching and pagination."""
        logger.debug(f"Fetching notifications for user {user_id} (limit: {limit}, offset: {offset}, unread_only: {unread_only})")
        
        query = cls.query.filter_by(user_id=user_id)
        
        if unread_only:
            query = query.filter_by(read=False)
        
        notifications = query.order_by(cls.created_at.desc()).offset(offset).limit(limit).all()
        
        log_db_query("SELECT", "notifications", None, f"user_notifications_{user_id}")
        logger.debug(f"Retrieved {len(notifications)} notifications for user {user_id}")
        
        return notifications

    @classmethod
    @cache.cached(timeout=180, key_prefix='user_recent_notifications')
    def get_recent_notifications(cls, user_id, hours=24):
        """Get recent notifications for a user with caching."""
        logger.debug(f"Fetching recent notifications for user {user_id} (last {hours} hours)")
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        notifications = cls.query.filter(
            cls.user_id == user_id,
            cls.created_at >= cutoff_time
        ).order_by(cls.created_at.desc()).all()
        
        log_db_query("SELECT", "notifications", None, f"recent_notifications_{user_id}")
        logger.debug(f"Retrieved {len(notifications)} recent notifications for user {user_id}")
        
        return notifications

    @classmethod
    def mark_all_as_read(cls, user_id):
        """Mark all notifications as read for a user with logging and cache management."""
        logger.info(f"Marking all notifications as read for user {user_id}")
        
        try:
            notifications = cls.query.filter_by(user_id=user_id, read=False).all()
            count = len(notifications)
            
            if count == 0:
                logger.debug(f"No unread notifications found for user {user_id}")
                return 0
            
            current_time = datetime.utcnow()
            for notification in notifications:
                notification.read = True
                notification.read_at = current_time
            
            db.session.commit()
            
            logger.info(f"Successfully marked {count} notifications as read for user {user_id}")
            log_db_query("UPDATE", "notifications", None, f"bulk_mark_read_{count}_notifications")
            
            # Invalidate user's notification caches
            invalidate_user_cache(user_id, CacheKeys.USER_NOTIFICATIONS)
            cache.delete(f'user_unread_count_{user_id}')
            cache.delete(f'user_recent_notifications_{user_id}')
            
            return count
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to mark all notifications as read for user {user_id}: {str(e)}")
            raise

    @classmethod
    def bulk_delete_notifications(cls, user_id, notification_ids):
        """Delete multiple notifications for a user with logging."""
        logger.info(f"Bulk deleting {len(notification_ids)} notifications for user {user_id}")
        
        try:
            deleted_count = 0
            for notification_id in notification_ids:
                notification = cls.query.filter_by(id=notification_id, user_id=user_id).first()
                if notification:
                    db.session.delete(notification)
                    deleted_count += 1
                else:
                    logger.warning(f"Notification {notification_id} not found or doesn't belong to user {user_id}")
            
            db.session.commit()
            
            logger.info(f"Successfully deleted {deleted_count} notifications for user {user_id}")
            log_db_query("DELETE", "notifications", None, f"bulk_delete_{deleted_count}_notifications")
            
            # Invalidate user's notification caches
            invalidate_user_cache(user_id, CacheKeys.USER_NOTIFICATIONS)
            cache.delete(f'user_unread_count_{user_id}')
            cache.delete(f'user_recent_notifications_{user_id}')
            
            return deleted_count
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to bulk delete notifications for user {user_id}: {str(e)}")
            raise

    @classmethod
    def cleanup_old_notifications(cls, days=30):
        """Delete notifications older than specified days with comprehensive logging."""
        logger.info(f"Starting cleanup of notifications older than {days} days")
        
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            old_notifications = cls.query.filter(cls.created_at < cutoff_date).all()
            count = len(old_notifications)
            
            if count == 0:
                logger.info("No old notifications found for cleanup")
                return 0
            
            # Track affected users for cache invalidation
            affected_users = set()
            for notification in old_notifications:
                affected_users.add(notification.user_id)
                db.session.delete(notification)
            
            db.session.commit()
            
            logger.info(f"Successfully cleaned up {count} old notifications affecting {len(affected_users)} users")
            log_db_query("DELETE", "notifications", None, f"cleanup_{count}_old_notifications")
            
            # Invalidate caches for affected users
            for user_id in affected_users:
                invalidate_user_cache(user_id, CacheKeys.USER_NOTIFICATIONS)
                cache.delete(f'user_unread_count_{user_id}')
                cache.delete(f'user_recent_notifications_{user_id}')
            
            return count
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to cleanup old notifications: {str(e)}")
            raise

    @classmethod
    def get_notification_stats(cls, user_id):
        """Get notification statistics for a user with caching."""
        cache_key = f'notification_stats_{user_id}'
        cached_stats = cache.get(cache_key)
        
        if cached_stats is not None:
            logger.debug(f"Cache hit for notification stats for user {user_id}")
            return cached_stats
        
        logger.debug(f"Calculating notification stats for user {user_id}")
        
        total_count = cls.query.filter_by(user_id=user_id).count()
        unread_count = cls.query.filter_by(user_id=user_id, read=False).count()
        
        # Count by notification type
        type_counts = {}
        for notification_type in NotificationType:
            count = cls.query.filter_by(user_id=user_id, type=notification_type).count()
            type_counts[notification_type.value] = count
        
        stats = {
            'total_notifications': total_count,
            'unread_notifications': unread_count,
            'read_notifications': total_count - unread_count,
            'by_type': type_counts,
            'read_percentage': (total_count - unread_count) / total_count * 100 if total_count > 0 else 0
        }
        
        # Cache for 5 minutes
        cache.set(cache_key, stats, timeout=300)
        log_db_query("SELECT", "notifications", None, f"stats_calculation_user_{user_id}")
        
        logger.debug(f"Calculated stats for user {user_id}: {stats}")
        return stats

    def to_dict(self, include_related_objects=False):
        """Convert notification to dictionary with optional related objects."""
        result = {
            'id': self.id,
            'user_id': self.user_id,
            'task_id': self.task_id,
            'type': self.type.value,
            'title': self.title,
            'message': self.message,
            'related_user_id': self.related_user_id,
            'project_id': self.project_id,
            'sprint_id': self.sprint_id,
            'read': self.read,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'created_at': self.created_at.isoformat()
        }
        
        if include_related_objects:
            result.update({
                'task': self.task.to_dict() if self.task else None,
                'related_user': {
                    'id': self.related_user.id,
                    'name': self.related_user.name,
                    'avatar_url': self.related_user.avatar_url
                } if self.related_user else None,
                'project': {
                    'id': self.project.id,
                    'name': self.project.name
                } if self.project else None,
                'sprint': {
                    'id': self.sprint.id,
                    'name': self.sprint.name
                } if self.sprint else None
            })
        
        return result

    @classmethod
    def create_task_notification(cls, task, notification_type, related_user_id=None):
        """Create a task-related notification with smart messaging."""
        logger.debug(f"Creating task notification: {notification_type.value} for task {task.id}")
        
        # Generate context-aware messages
        message_templates = {
            NotificationType.TASK_ASSIGNED: f"Task '{task.name}' has been assigned to you",
            NotificationType.TASK_STATUS_CHANGED: f"Task '{task.name}' status changed to {task.status.value}",
            NotificationType.TASK_DUE_SOON: f"Task '{task.name}' is due soon",
            NotificationType.TASK_OVERDUE: f"Task '{task.name}' is overdue",
            NotificationType.TASK_COMPLETED: f"Task '{task.name}' has been completed",
            NotificationType.TASK_COMMENT: f"New comment on task '{task.name}'"
        }
        
        title = f"Task Update: {task.name[:50]}..."
        message = message_templates.get(notification_type, f"Task '{task.name}' has been updated")
        
        return cls.create_notification(
            user_id=task.assigned_to_id,
            notification_type=notification_type,
            title=title,
            message=message,
            task_id=task.id,
            related_user_id=related_user_id,
            project_id=task.project_id
        )

    def __repr__(self):
        return f'<Notification {self.id}: {self.type.value} for User {self.user_id}>'