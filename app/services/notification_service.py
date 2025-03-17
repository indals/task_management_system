from app.models.notification import Notification
from app.models.user import User
from app.models.task import Task
from app import db

class NotificationService:
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

