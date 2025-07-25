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
    
    # Profile information
    avatar_url = db.Column(db.String(500))
    bio = db.Column(db.Text)
    skills = db.Column(db.Text)  # JSON string of skills
    github_username = db.Column(db.String(100))
    linkedin_url = db.Column(db.String(500))
    phone = db.Column(db.String(20))
    timezone = db.Column(db.String(50), default='UTC')
    
    # Work preferences
    daily_work_hours = db.Column(db.Float, default=8.0)
    hourly_rate = db.Column(db.Float)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Task relationships
    created_tasks = db.relationship('Task', foreign_keys='Task.created_by_id', back_populates='creator', cascade='all, delete-orphan')
    # assigned_tasks = db.relationship('Task', foreign_keys='Task.assigned_to_id', back_populates='assignee')
    assigned_tasks = db.relationship('Task', foreign_keys='Task.assigned_to_id', back_populates='assignee')

    
    # Project relationships
    owned_projects = db.relationship('Project', back_populates='owner', cascade='all, delete-orphan')
    project_memberships = db.relationship('ProjectMember', back_populates='user', cascade='all, delete-orphan')
    
    # Other relationships
    notifications = db.relationship('Notification', back_populates='user', foreign_keys='Notification.user_id')
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
            user.last_login = datetime.utcnow()
            db.session.commit()
            return user
        return None

    def update_profile(self, name=None, email=None, bio=None, skills=None, 
                      github_username=None, linkedin_url=None, phone=None, 
                      timezone=None, daily_work_hours=None, hourly_rate=None):
        if email and User.query.filter(User.email == email, User.id != self.id).first():
            raise ValueError("Email already in use by another user")
        
        if name:
            self.name = name
        if email:
            self.email = email
        if bio is not None:
            self.bio = bio
        if skills is not None:
            self.skills = skills
        if github_username is not None:
            self.github_username = github_username
        if linkedin_url is not None:
            self.linkedin_url = linkedin_url
        if phone is not None:
            self.phone = phone
        if timezone is not None:
            self.timezone = timezone
        if daily_work_hours is not None:
            self.daily_work_hours = daily_work_hours
        if hourly_rate is not None:
            self.hourly_rate = hourly_rate
            
        db.session.commit()

    def assign_task(self, task):
        if task.assigned_to_id is not None:
            raise ValueError("Task is already assigned to someone else.")
        task.assigned_to_id = self.id
        db.session.commit()

    def get_tasks(self):
        return self.assigned_tasks

    def get_projects(self):
        """Get all projects user is involved in (owned or member)."""
        owned = self.owned_projects
        member_projects = [membership.project for membership in self.project_memberships]
        return list(set(owned + member_projects))

    def get_project_role(self, project_id):
        """Get user's role in a specific project."""
        membership = next((m for m in self.project_memberships if m.project_id == project_id), None)
        return membership.role if membership else None

    def has_project_permission(self, project_id, permission):
        """Check if user has specific permission in a project."""
        # Project owner has all permissions
        if any(p.id == project_id for p in self.owned_projects):
            return True
        
        # Check project membership permissions
        membership = next((m for m in self.project_memberships if m.project_id == project_id), None)
        return membership.has_permission(permission) if membership else False

    def get_workload(self):
        """Calculate user's current workload based on active tasks."""
        active_tasks = [task for task in self.assigned_tasks 
                       if task.status.value not in ['DONE', 'CANCELLED']]
        
        total_hours = sum(task.estimated_hours or 0 for task in active_tasks)
        return {
            'active_tasks_count': len(active_tasks),
            'estimated_hours': total_hours,
            'workload_percentage': min((total_hours / (self.daily_work_hours * 5)) * 100, 100) if self.daily_work_hours else 0
        }

    def add_skill(self, skill):
        """Add a skill to user's profile."""
        import json
        skills = []
        if self.skills:
            try:
                skills = json.loads(self.skills)
            except json.JSONDecodeError:
                skills = []
        
        if skill not in skills:
            skills.append(skill)
            self.skills = json.dumps(skills)
            db.session.commit()

    def remove_skill(self, skill):
        """Remove a skill from user's profile."""
        import json
        skills = []
        if self.skills:
            try:
                skills = json.loads(self.skills)
            except json.JSONDecodeError:
                return
        
        if skill in skills:
            skills.remove(skill)
            self.skills = json.dumps(skills)
            db.session.commit()

    def to_dict(self, include_sensitive=False):
        import json
        
        # Parse skills from JSON string
        skills_list = []
        if self.skills:
            try:
                skills_list = json.loads(self.skills)
            except json.JSONDecodeError:
                skills_list = []

        result = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role.value,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            'skills': skills_list,
            'github_username': self.github_username,
            'linkedin_url': self.linkedin_url,
            'timezone': self.timezone,
            'daily_work_hours': self.daily_work_hours,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_sensitive:
            result.update({
                'phone': self.phone,
                'hourly_rate': self.hourly_rate
            })
            
        return result

    @classmethod
    def get_all_user_ids_and_names(cls):
        users = cls.query.filter_by(is_active=True).all()
        return [{"id": user.id, "name": user.name, "role": user.role.value} for user in users]

    def deactivate(self):
        """Deactivate user account."""
        self.is_active = False
        db.session.commit()

    def activate(self):
        """Activate user account."""
        self.is_active = True
        db.session.commit()
