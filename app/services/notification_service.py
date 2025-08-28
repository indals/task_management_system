from app.models.notification import Notification
from app.models.user import User
from app.models.task import Task
from app import db
from app.utils.cache_utils import cache, cached_per_user, CacheKeys, invalidate_user_cache, invalidate_project_cache


class NotificationService:


    # Add this method to app/services/notification_service.py

    @staticmethod
    def get_notification_summary(user_id):
        """Get notification summary with counts and recent notifications."""
        try:
            # Get total unread count
            unread_count = Notification.query.filter_by(user_id=user_id, read=False).count()
            
            # Get recent notifications (last 5)
            recent_notifications = Notification.query.filter_by(user_id=user_id)\
                .order_by(Notification.created_at.desc())\
                .limit(5)\
                .all()
            
            # Get count by notification type
            from sqlalchemy import func
            type_counts = db.session.query(
                Notification.type, 
                func.count(Notification.id)
            ).filter(
                Notification.user_id == user_id,
                Notification.read == False
            ).group_by(Notification.type).all()
            
            type_summary = {}
            for notification_type, count in type_counts:
                type_summary[notification_type.value] = count
            
            return {
                'unread_count': unread_count,
                'recent_notifications': [n.to_dict() for n in recent_notifications],
                'type_summary': type_summary,
                'total_notifications': Notification.query.filter_by(user_id=user_id).count()
            }
            
        except Exception as e:
            return {'error': f'Error getting notification summary: {str(e)}'}
    
    @staticmethod
    def get_user_notifications(user_id, unread_only=False):
        query = Notification.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(read=False)
        notifications = query.all()
        return [n.to_dict() for n in notifications]

    @staticmethod
    def mark_as_read(notification_id, user_id):
        notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if not notification:
            return {'error': 'Notification not found'}
        notification.read = True
        db.session.commit()
        return notification.to_dict()

    @staticmethod
    def mark_all_notifications_as_read(user_id):
        notifications = Notification.query.filter_by(user_id=user_id, read=False).all()
        for notification in notifications:
            notification.read = True
        db.session.commit()
        return {'message': 'All notifications marked as read'}

    @staticmethod
    def delete_notification(notification_id, user_id):
        notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if not notification:
            return {'error': 'Notification not found'}
        db.session.delete(notification)
        db.session.commit()

