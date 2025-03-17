from app import db
from datetime import datetime

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete="CASCADE"))
    message = db.Column(db.String(200), nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", backref="user_notifications")  # Change backref name to something else
    task = db.relationship("Task", backref="task_notifications")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'task_id': self.task_id,
            'message': self.message,
            'read': self.read,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
