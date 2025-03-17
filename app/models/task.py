from app import db
from datetime import datetime
from .enums import TaskStatus, TaskPriority
from .task_comment import TaskComment

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    priority = db.Column(db.Enum(TaskPriority), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define the assignee relationship
    assignee = db.relationship('User', foreign_keys=[assigned_to_id], back_populates='assigned_tasks')

    # Creator relationship
    creator = db.relationship('User', foreign_keys=[created_by_id], back_populates='created_tasks')

    # Use a unique backref name for the comments relationship
    comments = db.relationship('TaskComment', backref='task_instance', cascade='all, delete-orphan', single_parent=True)
    notifications = db.relationship('Notification', back_populates='task', lazy='dynamic', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'priority': self.priority.value,
            'assigned_to': self.assignee.to_dict() if self.assignee else None,
            'created_by': self.creator.to_dict() if self.creator else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

