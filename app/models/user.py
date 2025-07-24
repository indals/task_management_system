# app/models/user.py
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .enums import UserRole

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Task relationships
    created_tasks = db.relationship('Task', foreign_keys='Task.created_by_id', back_populates='creator', cascade='all, delete-orphan')
    assigned_tasks = db.relationship('Task', foreign_keys='Task.assigned_to_id', back_populates='assignee')
    
    # Other relationships
    notifications = db.relationship('Notification', back_populates='user', cascade='all, delete-orphan')
    owned_projects = db.relationship('Project', back_populates='owner', cascade='all, delete-orphan')
    task_comments = db.relationship('TaskComment', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def register(cls, name, email, password, role):
        if cls.query.filter_by(email=email).first():
            raise ValueError("Email already registered")
        user = cls(name=name, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def login(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None

    def update_profile(self, name, email):
        if User.query.filter(User.email == email, User.id != self.id).first():
            raise ValueError("Email already in use by another user")
        self.name = name
        self.email = email
        db.session.commit()

    def assign_task(self, task):
        if task.assigned_to_id is not None:
            raise ValueError("Task is already assigned to someone else.")
        task.assigned_to_id = self.id
        db.session.commit()

    def get_tasks(self):
        return self.assigned_tasks

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def get_all_user_ids_and_names(cls):
        users = cls.query.all()
        return [{"id": user.id, "name": user.name} for user in users]
