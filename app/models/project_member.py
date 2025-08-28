# app/models/project_member.py
from app import db
from datetime import datetime

# Import logging and caching utilities
from app.utils.logger import get_logger, log_db_query
from app.utils.cache_utils import cache, cached_per_user, invalidate_user_cache, CacheKeys

# Initialize logger for this module
logger = get_logger('project_members')

class ProjectMember(db.Model):
    __tablename__ = 'project_members'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    role = db.Column(db.String(100))  # Role in this specific project
    
    # Permissions
    can_create_tasks = db.Column(db.Boolean, default=True)
    can_edit_tasks = db.Column(db.Boolean, default=True)
    can_delete_tasks = db.Column(db.Boolean, default=False)
    can_manage_sprints = db.Column(db.Boolean, default=False)
    can_manage_members = db.Column(db.Boolean, default=False)
    
    # Timestamps
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', back_populates='team_members')
    user = db.relationship('User', back_populates='project_memberships')

    # Unique constraint to prevent duplicate memberships
    __table_args__ = (db.UniqueConstraint('project_id', 'user_id', name='unique_project_member'),)

    @classmethod
    def add_member(cls, project_id, user_id, role=None, permissions=None):
        """Add a new project member with logging and cache management."""
        logger.info(f"Adding user {user_id} to project {project_id} with role: {role}")
        
        # Check if membership already exists
        existing = cls.query.filter_by(project_id=project_id, user_id=user_id).first()
        if existing:
            logger.warning(f"Member addition failed: User {user_id} already member of project {project_id}")
            raise ValueError("User is already a member of this project")
        
        # Create new membership
        member = cls(
            project_id=project_id,
            user_id=user_id,
            role=role or "Developer"
        )
        
        # Set permissions if provided
        if permissions:
            for perm, value in permissions.items():
                if hasattr(member, f'can_{perm}'):
                    setattr(member, f'can_{perm}', value)
                    logger.debug(f"Set permission {perm}={value} for user {user_id} in project {project_id}")
        
        try:
            db.session.add(member)
            db.session.commit()
            
            logger.info(f"Successfully added user {user_id} to project {project_id}")
            log_db_query("INSERT", "project_members", member.id)
            
            # Invalidate related caches
            invalidate_user_cache(user_id, CacheKeys.USER_PROJECTS)
            cache.delete(f'project_members_{project_id}')
            cache.delete(f'project_team_{project_id}')
            
            return member
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to add user {user_id} to project {project_id}: {str(e)}")
            raise

    @classmethod
    def remove_member(cls, project_id, user_id):
        """Remove a project member with logging and cache management."""
        logger.info(f"Removing user {user_id} from project {project_id}")
        
        member = cls.query.filter_by(project_id=project_id, user_id=user_id).first()
        if not member:
            logger.warning(f"Member removal failed: User {user_id} not found in project {project_id}")
            raise ValueError("User is not a member of this project")
        
        try:
            member_id = member.id
            db.session.delete(member)
            db.session.commit()
            
            logger.info(f"Successfully removed user {user_id} from project {project_id}")
            log_db_query("DELETE", "project_members", member_id)
            
            # Invalidate related caches
            invalidate_user_cache(user_id, CacheKeys.USER_PROJECTS)
            cache.delete(f'project_members_{project_id}')
            cache.delete(f'project_team_{project_id}')
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to remove user {user_id} from project {project_id}: {str(e)}")
            raise

    @classmethod 
    @cache.cached(timeout=300, key_prefix='project_members')
    def get_project_members(cls, project_id):
        """Get all members of a project with caching."""
        logger.debug(f"Fetching members for project {project_id}")
        log_db_query("SELECT", "project_members", None, f"project_id={project_id}")
        return cls.query.filter_by(project_id=project_id).all()

    @classmethod
    @cache.cached(timeout=600, key_prefix='project_team')
    def get_project_team_details(cls, project_id):
        """Get detailed team information for a project with caching."""
        logger.debug(f"Fetching team details for project {project_id}")
        
        members = cls.query.filter_by(project_id=project_id).all()
        team_data = []
        
        for member in members:
            member_info = member.to_dict()
            # Include user details for easier access
            if member.user:
                member_info['user_name'] = member.user.name
                member_info['user_email'] = member.user.email
                member_info['user_avatar'] = member.user.avatar_url
            team_data.append(member_info)
        
        logger.debug(f"Retrieved {len(team_data)} team members for project {project_id}")
        return team_data

    def update_role(self, new_role):
        """Update member's role with logging and cache invalidation."""
        old_role = self.role
        logger.info(f"Updating role for user {self.user_id} in project {self.project_id}: {old_role} -> {new_role}")
        
        self.role = new_role
        
        try:
            db.session.commit()
            logger.info(f"Role updated successfully for user {self.user_id} in project {self.project_id}")
            log_db_query("UPDATE", "project_members", self.id, f"role={new_role}")
            
            # Invalidate related caches
            invalidate_user_cache(self.user_id, CacheKeys.USER_PROJECTS)
            cache.delete(f'project_members_{self.project_id}')
            cache.delete(f'project_team_{self.project_id}')
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to update role for user {self.user_id} in project {self.project_id}: {str(e)}")
            raise

    def update_permissions(self, permissions):
        """Update user permissions for this project with logging and cache invalidation."""
        logger.info(f"Updating permissions for user {self.user_id} in project {self.project_id}")
        
        changes = []
        for permission, value in permissions.items():
            if hasattr(self, f'can_{permission}'):
                old_value = getattr(self, f'can_{permission}')
                if old_value != value:
                    setattr(self, f'can_{permission}', value)
                    changes.append(f"{permission}: {old_value} -> {value}")
                    logger.debug(f"Permission {permission} changed from {old_value} to {value}")
        
        if changes:
            try:
                db.session.commit()
                logger.info(f"Permissions updated for user {self.user_id} in project {self.project_id}: {', '.join(changes)}")
                log_db_query("UPDATE", "project_members", self.id, f"permissions_updated")
                
                # Invalidate related caches
                invalidate_user_cache(self.user_id, CacheKeys.USER_PROJECTS)
                cache.delete(f'project_members_{self.project_id}')
                cache.delete(f'project_team_{self.project_id}')
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Failed to update permissions for user {self.user_id} in project {self.project_id}: {str(e)}")
                raise
        else:
            logger.debug(f"No permission changes for user {self.user_id} in project {self.project_id}")

    def has_permission(self, permission):
        """Check if user has specific permission with logging."""
        permission_map = {
            'create_tasks': self.can_create_tasks,
            'edit_tasks': self.can_edit_tasks,
            'delete_tasks': self.can_delete_tasks,
            'manage_sprints': self.can_manage_sprints,
            'manage_members': self.can_manage_members
        }
        
        has_perm = permission_map.get(permission, False)
        logger.debug(f"Permission check for user {self.user_id} in project {self.project_id}: {permission}={has_perm}")
        return has_perm

    def get_all_permissions(self):
        """Get all permissions for this member with caching consideration."""
        permissions = {
            'create_tasks': self.can_create_tasks,
            'edit_tasks': self.can_edit_tasks,
            'delete_tasks': self.can_delete_tasks,
            'manage_sprints': self.can_manage_sprints,
            'manage_members': self.can_manage_members
        }
        
        logger.debug(f"Retrieved all permissions for user {self.user_id} in project {self.project_id}")
        return permissions

    @classmethod
    def get_user_project_role(cls, user_id, project_id):
        """Get user's role in a specific project with caching."""
        cache_key = f'user_project_role_{user_id}_{project_id}'
        cached_role = cache.get(cache_key)
        
        if cached_role is not None:
            logger.debug(f"Cache hit for user {user_id} role in project {project_id}")
            return cached_role
        
        logger.debug(f"Fetching role for user {user_id} in project {project_id}")
        member = cls.query.filter_by(user_id=user_id, project_id=project_id).first()
        role = member.role if member else None
        
        # Cache for 10 minutes
        cache.set(cache_key, role, timeout=600)
        log_db_query("SELECT", "project_members", member.id if member else None, f"user_role_check")
        
        return role

    @classmethod
    def bulk_update_permissions(cls, project_id, user_permissions_map):
        """Bulk update permissions for multiple users with logging."""
        logger.info(f"Bulk updating permissions for {len(user_permissions_map)} users in project {project_id}")
        
        updated_count = 0
        errors = []
        
        for user_id, permissions in user_permissions_map.items():
            try:
                member = cls.query.filter_by(project_id=project_id, user_id=user_id).first()
                if member:
                    member.update_permissions(permissions)
                    updated_count += 1
                else:
                    errors.append(f"User {user_id} not found in project {project_id}")
                    
            except Exception as e:
                errors.append(f"Failed to update user {user_id}: {str(e)}")
                logger.error(f"Error in bulk permission update for user {user_id}: {str(e)}")
        
        logger.info(f"Bulk permission update completed: {updated_count} successful, {len(errors)} errors")
        
        if errors:
            logger.warning(f"Bulk update errors: {'; '.join(errors)}")
        
        return {'updated_count': updated_count, 'errors': errors}

    def to_dict(self, include_user_details=False, include_project_details=False):
        """Convert member to dictionary with optional details and caching consideration."""
        result = {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'role': self.role,
            'permissions': self.get_all_permissions(),
            'joined_at': self.joined_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_user_details and self.user:
            result['user'] = {
                'name': self.user.name,
                'email': self.user.email,
                'avatar_url': self.user.avatar_url,
                'role': self.user.role.value if self.user.role else None
            }
        
        if include_project_details and self.project:
            result['project'] = {
                'name': self.project.name,
                'description': self.project.description,
                'status': self.project.status.value if self.project.status else None
            }
        
        return result

    def __repr__(self):
        return f'<ProjectMember {self.user_id} in Project {self.project_id} as {self.role}>'