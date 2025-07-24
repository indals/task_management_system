# app/models/task.py
from app import db
from datetime import datetime
from .enums import TaskStatus, TaskPriority

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

    # User relationships
    assignee = db.relationship('User', foreign_keys=[assigned_to_id], back_populates='assigned_tasks')
    creator = db.relationship('User', foreign_keys=[created_by_id], back_populates='created_tasks')
    
    # Child relationships
    comments = db.relationship('TaskComment', back_populates='task', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', back_populates='task', cascade='all, delete-orphan')

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
            'updated_at': self.updated_at.isoformat(),
            'comments_count': len(self.comments)
        }

