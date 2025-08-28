# app/models/project.py
from app import db
from datetime import datetime
import json
from app.utils.logger import get_logger, log_db_query
from app.utils.cache_utils import cache, cached_per_user, invalidate_user_cache, invalidate_project_cache, CacheKeys
from app.models.project_member import ProjectMember
from .enums import ProjectStatus

# Initialize logger for this module
logger = get_logger('projects')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(ProjectStatus), nullable=False, default=ProjectStatus.PLANNING)
    
    # Project details
    repository_url = db.Column(db.String(500))
    documentation_url = db.Column(db.String(500))
    technology_stack = db.Column(db.Text)  # JSON string of technologies
    
    # Time tracking
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    estimated_hours = db.Column(db.Float)
    
    # Project metrics
    priority = db.Column(db.String(20), default='MEDIUM')
    budget = db.Column(db.Float)
    completion_percentage = db.Column(db.Float, default=0.0)
    
    # Ownership
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    # Client information
    client_name = db.Column(db.String(200))
    client_email = db.Column(db.String(120))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = db.relationship('User', back_populates='owned_projects')
    tasks = db.relationship('Task', back_populates='project', cascade='all, delete-orphan')
    sprints = db.relationship('Sprint', back_populates='project', cascade='all, delete-orphan')
    team_members = db.relationship('ProjectMember', back_populates='project', cascade='all, delete-orphan')

    @classmethod
    def create_project(cls, name, owner_id, description=None, technology_stack=None, 
                      start_date=None, end_date=None, estimated_hours=None, 
                      client_name=None, client_email=None, priority='MEDIUM', budget=None):
        """Create a new project with validation, logging and cache management."""
        logger.info(f"Creating project '{name}' owned by user {owner_id}")
        
        # Validation
        if not name or not name.strip():
            logger.warning(f"Project creation failed: Empty name for owner {owner_id}")
            raise ValueError("Project name cannot be empty")
        
        if start_date and end_date and start_date >= end_date:
            logger.warning(f"Project creation failed: Invalid date range for '{name}'")
            raise ValueError("Start date must be before end date")
        
        # Check for duplicate project names for the same owner
        existing = cls.query.filter_by(name=name.strip(), owner_id=owner_id).first()
        if existing:
            logger.warning(f"Project creation failed: Duplicate name '{name}' for owner {owner_id}")
            raise ValueError("You already have a project with this name")
        
        try:
            project = cls(
                name=name.strip(),
                description=description.strip() if description else None,
                owner_id=owner_id,
                technology_stack=json.dumps(technology_stack) if technology_stack else None,
                start_date=start_date,
                end_date=end_date,
                estimated_hours=estimated_hours,
                client_name=client_name.strip() if client_name else None,
                client_email=client_email.strip() if client_email else None,
                priority=priority,
                budget=budget
            )
            
            db.session.add(project)
            db.session.commit()
            
            logger.info(f"Project created successfully: ID {project.id} - '{name}'")
            
            # Invalidate related caches
            invalidate_user_cache(owner_id, CacheKeys.USER_PROJECTS)
            cache.delete('all_projects_list')
            cache.delete('recent_projects')
            
            # Log database query for monitoring
            log_db_query("Project", "CREATE", project.id, {
                "name": name,
                "owner_id": owner_id,
                "estimated_hours": estimated_hours
            })
            
            return project
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to create project '{name}': {str(e)}")
            raise

    def update_project(self, name=None, description=None, status=None, repository_url=None,
                      documentation_url=None, technology_stack=None, start_date=None, 
                      end_date=None, estimated_hours=None, client_name=None, 
                      client_email=None, priority=None, budget=None):
        """Update project with validation, logging and cache invalidation."""
        logger.info(f"Updating project {self.id}")
        
        changes = []
        
        # Validate date changes
        new_start = start_date if start_date is not None else self.start_date
        new_end = end_date if end_date is not None else self.end_date
        
        if new_start and new_end and new_start >= new_end:
            logger.warning(f"Project update failed: Invalid date range for project {self.id}")
            raise ValueError("Start date must be before end date")
        
        # Check for duplicate names if name is changing
        if name and name.strip() != self.name:
            existing = Project.query.filter(
                Project.name == name.strip(),
                Project.owner_id == self.owner_id,
                Project.id != self.id
            ).first()
            if existing:
                logger.warning(f"Project update failed: Duplicate name '{name}' for owner {self.owner_id}")
                raise ValueError("You already have a project with this name")
        
        # Track changes for logging
        if name is not None and name.strip() != self.name:
            changes.append(f"name: '{self.name}' -> '{name.strip()}'")
            self.name = name.strip()
        
        if description is not None and description != self.description:
            changes.append("description updated")
            self.description = description.strip() if description else None
        
        if status is not None and status != self.status:
            changes.append(f"status: {self.status.value} -> {status.value}")
            self.status = status
        
        if repository_url is not None and repository_url != self.repository_url:
            changes.append("repository_url updated")
            self.repository_url = repository_url.strip() if repository_url else None
        
        if documentation_url is not None and documentation_url != self.documentation_url:
            changes.append("documentation_url updated")
            self.documentation_url = documentation_url.strip() if documentation_url else None
        
        if technology_stack is not None:
            new_tech_json = json.dumps(technology_stack) if technology_stack else None
            if new_tech_json != self.technology_stack:
                changes.append("technology_stack updated")
                self.technology_stack = new_tech_json
        
        if start_date is not None and start_date != self.start_date:
            changes.append(f"start_date: {self.start_date} -> {start_date}")
            self.start_date = start_date
        
        if end_date is not None and end_date != self.end_date:
            changes.append(f"end_date: {self.end_date} -> {end_date}")
            self.end_date = end_date
        
        if estimated_hours is not None and estimated_hours != self.estimated_hours:
            changes.append(f"estimated_hours: {estimated_hours}")
            self.estimated_hours = estimated_hours
        
        if client_name is not None and client_name != self.client_name:
            changes.append("client_name updated")
            self.client_name = client_name.strip() if client_name else None
        
        if client_email is not None and client_email != self.client_email:
            changes.append("client_email updated")
            self.client_email = client_email.strip() if client_email else None
        
        if priority is not None and priority != self.priority:
            changes.append(f"priority: {priority}")
            self.priority = priority
        
        if budget is not None and budget != self.budget:
            changes.append(f"budget: {budget}")
            self.budget = budget
        
        if changes:
            try:
                db.session.commit()
                logger.info(f"Project {self.id} updated: {', '.join(changes)}")
                
                # Invalidate related caches
                self._invalidate_project_caches()
                
                # Log database query for monitoring
                log_db_query("Project", "UPDATE", self.id)
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Failed to update project {self.id}: {str(e)}")
                raise
        else:
            logger.debug(f"No changes in project update for project {self.id}")

    def delete_project(self):
        """Delete project with cascade cleanup and comprehensive logging."""
        logger.info(f"Deleting project {self.id} - '{self.name}'")
        
        project_id = self.id
        project_name = self.name
        owner_id = self.owner_id
        tasks_count = len(self.tasks)
        sprints_count = len(self.sprints)
        members_count = len(self.team_members)
        
        try:
            db.session.delete(self)
            db.session.commit()
            
            logger.info(f"Project {project_id} deleted successfully: {tasks_count} tasks, {sprints_count} sprints, {members_count} members")
            
            # Invalidate related caches
            invalidate_user_cache(owner_id, CacheKeys.USER_PROJECTS)
            invalidate_project_cache(project_id)
            cache.delete('all_projects_list')
            cache.delete('recent_projects')
            
            # Invalidate caches for all team members
            for member in self.team_members:
                invalidate_user_cache(member.user_id, CacheKeys.USER_PROJECTS)
            
            # Log database query for monitoring
            log_db_query("Project", "DELETE", project_id, {
                "name": project_name,
                "tasks_count": tasks_count,
                "sprints_count": sprints_count,
                "members_count": members_count
            })
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to delete project {project_id}: {str(e)}")
            raise

    @cache.cached(timeout=300, key_prefix='project_metrics')
    def get_project_metrics(self):
        """Get comprehensive project metrics with caching."""
        logger.debug(f"Calculating metrics for project {self.id}")
        
        tasks = self.tasks
        sprints = self.sprints
        total_tasks = len(tasks)
        
        if total_tasks == 0:
            return {
                'total_tasks': 0,
                'completed_tasks': 0,
                'in_progress_tasks': 0,
                'todo_tasks': 0,
                'completion_percentage': 0,
                'total_story_points': 0,
                'completed_story_points': 0,
                'total_sprints': len(sprints),
                'active_sprints': 0,
                'completed_sprints': 0,
                'estimated_vs_actual_hours': {'estimated': self.estimated_hours or 0, 'actual': 0},
                'team_size': len(self.team_members)
            }
        
        # Task analysis
        completed_tasks = [t for t in tasks if t.status.value == 'DONE']
        in_progress_tasks = [t for t in tasks if t.status.value == 'IN_PROGRESS']
        todo_tasks = [t for t in tasks if t.status.value == 'TODO']
        
        # Story points calculation
        total_story_points = sum(task.story_points or 0 for task in tasks)
        completed_story_points = sum(task.story_points or 0 for task in completed_tasks)
        
        # Sprint analysis
        from .enums import SprintStatus
        active_sprints = sum(1 for s in sprints if s.status == SprintStatus.ACTIVE)
        completed_sprints = sum(1 for s in sprints if s.status == SprintStatus.COMPLETED)
        
        # Time tracking
        actual_hours = sum(task.actual_hours or 0 for task in tasks)
        
        metrics = {
            'total_tasks': total_tasks,
            'completed_tasks': len(completed_tasks),
            'in_progress_tasks': len(in_progress_tasks),
            'todo_tasks': len(todo_tasks),
            'completion_percentage': (len(completed_tasks) / total_tasks) * 100,
            'total_story_points': total_story_points,
            'completed_story_points': completed_story_points,
            'story_points_completion': (completed_story_points / total_story_points * 100) if total_story_points > 0 else 0,
            'total_sprints': len(sprints),
            'active_sprints': active_sprints,
            'completed_sprints': completed_sprints,
            'estimated_vs_actual_hours': {
                'estimated': self.estimated_hours or 0,
                'actual': actual_hours
            },
            'team_size': len(self.team_members),
            'avg_task_completion_time': self._calculate_avg_completion_time(completed_tasks)
        }
        
        logger.debug(f"Project {self.id} metrics: {metrics['completion_percentage']:.1f}% complete")
        return metrics

    def _calculate_avg_completion_time(self, completed_tasks):
        """Calculate average task completion time in hours."""
        completion_times = []
        for task in completed_tasks:
            if hasattr(task, 'completed_at') and task.completed_at and task.created_at:
                duration = (task.completed_at - task.created_at).total_seconds() / 3600
                completion_times.append(duration)
        
        return sum(completion_times) / len(completion_times) if completion_times else 0

    def get_completion_percentage(self):
        """Calculate project completion based on tasks with caching consideration."""
        metrics = self.get_project_metrics()
        return metrics['completion_percentage']

    def update_completion_percentage(self):
        """Update the stored completion percentage and save to database."""
        new_percentage = self.get_completion_percentage()
        if abs(new_percentage - (self.completion_percentage or 0)) > 0.1:  # Only update if significant change
            logger.debug(f"Updating completion percentage for project {self.id}: {new_percentage:.1f}%")
            self.completion_percentage = new_percentage
            try:
                db.session.commit()
                self._invalidate_project_caches()
            except Exception as e:
                db.session.rollback()
                logger.error(f"Failed to update completion percentage for project {self.id}: {str(e)}")

    @cache.cached(timeout=600, key_prefix='project_team_members')
    def get_team_members(self):
        """Get all team members for this project with caching."""
        logger.debug(f"Fetching team members for project {self.id}")
        
        members = [member.user for member in self.team_members if member.user]
        logger.debug(f"Project {self.id} has {len(members)} team members")
        
        # Log database query for monitoring
        log_db_query("Project", "TEAM_MEMBERS", self.id, {"count": len(members)})
        
        return members

    def add_team_member(self, user_id, role=None):
        """Add a team member to the project with enhanced logging."""
        logger.info(f"Adding user {user_id} to project {self.id} with role {role}")
        
        existing_member = ProjectMember.query.filter_by(
            project_id=self.id, 
            user_id=user_id
        ).first()
        
        if existing_member:
            logger.warning(f"User {user_id} is already a member of project {self.id}")
            raise ValueError("User is already a team member")
        
        try:
            member = ProjectMember(
                project_id=self.id,
                user_id=user_id,
                role=role
            )
            
            db.session.add(member)
            db.session.commit()
            
            logger.info(f"User {user_id} added to project {self.id} successfully")
            
            # Invalidate related caches
            self._invalidate_project_caches()
            invalidate_user_cache(user_id, CacheKeys.USER_PROJECTS)
            
            # Log database query for monitoring
            log_db_query("ProjectMember", "CREATE", None, {
                "project_id": self.id,
                "user_id": user_id,
                "role": role
            })
            
            return member
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to add user {user_id} to project {self.id}: {str(e)}")
            raise

    def remove_team_member(self, user_id):
        """Remove a team member from the project with enhanced logging."""
        logger.info(f"Removing user {user_id} from project {self.id}")
        
        member = ProjectMember.query.filter_by(
            project_id=self.id, 
            user_id=user_id
        ).first()
        
        if not member:
            logger.warning(f"User {user_id} is not a member of project {self.id}")
            raise ValueError("User is not a team member")
        
        try:
            db.session.delete(member)
            db.session.commit()
            
            logger.info(f"User {user_id} removed from project {self.id} successfully")
            
            # Invalidate related caches
            self._invalidate_project_caches()
            invalidate_user_cache(user_id, CacheKeys.USER_PROJECTS)
            
            # Log database query for monitoring
            log_db_query("ProjectMember", "DELETE", None, {
                "project_id": self.id,
                "user_id": user_id
            })
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to remove user {user_id} from project {self.id}: {str(e)}")
            raise

    def update_team_member_role(self, user_id, new_role):
        """Update a team member's role with logging."""
        logger.info(f"Updating role for user {user_id} in project {self.id} to {new_role}")
        
        member = ProjectMember.query.filter_by(
            project_id=self.id,
            user_id=user_id
        ).first()
        
        if not member:
            logger.warning(f"User {user_id} is not a member of project {self.id}")
            raise ValueError("User is not a team member")
        
        old_role = member.role
        member.role = new_role
        
        try:
            db.session.commit()
            logger.info(f"Role updated for user {user_id} in project {self.id}: {old_role} -> {new_role}")
            
            # Invalidate related caches
            self._invalidate_project_caches()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to update role for user {user_id} in project {self.id}: {str(e)}")
            raise

    @cache.cached(timeout=300, key_prefix='project_active_sprint')
    def get_active_sprint(self):
        """Get the currently active sprint for this project with caching."""
        logger.debug(f"Fetching active sprint for project {self.id}")
        
        from .sprint import Sprint
        from .enums import SprintStatus
        
        active_sprint = Sprint.query.filter_by(
            project_id=self.id, 
            status=SprintStatus.ACTIVE
        ).first()
        
        if active_sprint:
            logger.debug(f"Project {self.id} has active sprint: {active_sprint.id}")
        else:
            logger.debug(f"Project {self.id} has no active sprint")
        
        return active_sprint

    def add_technology(self, technology):
        """Add a technology to the project stack with logging."""
        logger.info(f"Adding technology '{technology}' to project {self.id}")
        
        tech_stack = self._get_technology_list()
        
        if technology in tech_stack:
            logger.debug(f"Technology '{technology}' already exists in project {self.id}")
            return False
        
        tech_stack.append(technology)
        self.technology_stack = json.dumps(tech_stack)
        
        try:
            db.session.commit()
            logger.info(f"Technology '{technology}' added to project {self.id}")
            
            # Invalidate related caches
            self._invalidate_project_caches()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to add technology '{technology}' to project {self.id}: {str(e)}")
            raise

    def remove_technology(self, technology):
        """Remove a technology from the project stack with logging."""
        logger.info(f"Removing technology '{technology}' from project {self.id}")
        
        tech_stack = self._get_technology_list()
        
        if technology not in tech_stack:
            logger.debug(f"Technology '{technology}' not found in project {self.id}")
            return False
        
        tech_stack.remove(technology)
        self.technology_stack = json.dumps(tech_stack)
        
        try:
            db.session.commit()
            logger.info(f"Technology '{technology}' removed from project {self.id}")
            
            # Invalidate related caches
            self._invalidate_project_caches()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to remove technology '{technology}' from project {self.id}: {str(e)}")
            raise

    def _get_technology_list(self):
        """Get technology stack as a list with error handling."""
        if not self.technology_stack:
            return []
        
        try:
            return json.loads(self.technology_stack)
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON in technology_stack for project {self.id}")
            return []

    @classmethod
    @cache.cached(timeout=300, key_prefix='all_projects_list')
    def get_all_projects(cls, status_filter=None, owner_id=None, limit=None):
        """Get all projects with optional filtering and caching."""
        logger.debug(f"Fetching projects (status: {status_filter}, owner: {owner_id}, limit: {limit})")
        
        query = cls.query
        
        if status_filter:
            if isinstance(status_filter, str):
                status_filter = ProjectStatus(status_filter)
            query = query.filter_by(status=status_filter)
        
        if owner_id:
            query = query.filter_by(owner_id=owner_id)
        
        query = query.order_by(cls.updated_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        projects = query.all()
        logger.debug(f"Retrieved {len(projects)} projects")
        
        # Log database query for monitoring
        log_db_query("Project", "SELECT", None, {
            "status_filter": status_filter.value if status_filter else None,
            "owner_id": owner_id,
            "count": len(projects)
        })
        
        return projects

    @classmethod
    @cache.cached(timeout=180, key_prefix='recent_projects')
    def get_recent_projects(cls, limit=10):
        """Get recently updated projects with caching."""
        logger.debug(f"Fetching {limit} recent projects")
        
        projects = cls.query.order_by(cls.updated_at.desc()).limit(limit).all()
        logger.debug(f"Retrieved {len(projects)} recent projects")
        
        # Log database query for monitoring
        log_db_query("Project", "SELECT", None, {"recent_limit": limit, "count": len(projects)})
        
        return projects

    @classmethod
    def search_projects(cls, search_term, owner_id=None, status_filter=None, limit=None):
        """Search projects by name or description with logging."""
        logger.info(f"Searching projects with term: '{search_term}'")
        
        if not search_term or len(search_term.strip()) < 2:
            logger.warning("Search term too short or empty")
            return []
        
        query = cls.query.filter(
            db.or_(
                cls.name.ilike(f'%{search_term}%'),
                cls.description.ilike(f'%{search_term}%'),
                cls.technology_stack.ilike(f'%{search_term}%')
            )
        )
        
        if owner_id:
            query = query.filter_by(owner_id=owner_id)
        if status_filter:
            if isinstance(status_filter, str):
                status_filter = ProjectStatus(status_filter)
            query = query.filter_by(status=status_filter)
        
        query = query.order_by(cls.updated_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        projects = query.all()
        logger.info(f"Search returned {len(projects)} projects for term: '{search_term}'")
        
        # Log database query for monitoring
        log_db_query("Project", "SEARCH", None, {
            "search_term": search_term,
            "owner_id": owner_id,
            "status_filter": status_filter.value if status_filter else None,
            "count": len(projects)
        })
        
        return projects

    def is_overdue(self):
        """Check if project is overdue based on end date."""
        if not self.end_date:
            return False
        
        overdue = (
            self.status != ProjectStatus.COMPLETED and 
            datetime.utcnow() > self.end_date
        )
        
        if overdue:
            days_overdue = (datetime.utcnow() - self.end_date).days
            logger.info(f"Project {self.id} is overdue by {days_overdue} days")
        
        return overdue

    def days_remaining(self):
        """Get number of days remaining until project end date."""
        if not self.end_date or self.status == ProjectStatus.COMPLETED:
            return None
        
        now = datetime.utcnow()
        if now > self.end_date:
            return 0
        
        remaining = (self.end_date - now).days
        logger.debug(f"Project {self.id} has {remaining} days remaining")
        return remaining

    def can_be_edited_by(self, user):
        """Check if user can edit this project."""
        can_edit = (
            self.owner_id == user.id or 
            user.role.value in ['ADMIN', 'MANAGER'] or
            any(member.user_id == user.id and member.has_permission('edit_project') 
                for member in self.team_members)
        )
        
        logger.debug(f"Project {self.id} edit permission for user {user.id}: {can_edit}")
        return can_edit

    def can_be_deleted_by(self, user):
        """Check if user can delete this project."""
        can_delete = (
            self.owner_id == user.id or 
            user.role.value in ['ADMIN']
        )
        
        logger.debug(f"Project {self.id} delete permission for user {user.id}: {can_delete}")
        return can_delete

    def _invalidate_project_caches(self):
        """Helper method to invalidate all caches related to this project."""
        logger.debug(f"Invalidating all caches for project {self.id}")
        
        # Invalidate specific project caches
        cache.delete(f'project_metrics_{self.id}')
        cache.delete(f'project_team_members_{self.id}')
        cache.delete(f'project_active_sprint_{self.id}')
        
        # Invalidate general project caches
        cache.delete('all_projects_list')
        cache.delete('recent_projects')
        
        # Invalidate owner's project cache
        invalidate_user_cache(self.owner_id, CacheKeys.USER_PROJECTS)
        
        # Invalidate project-specific cache
        invalidate_project_cache(self.id)

    def to_dict(self, include_tasks=False, include_sprints=False, include_metrics=False, include_team=False):
        """Convert project to dictionary with enhanced options and caching consideration."""
        logger.debug(f"Converting project {self.id} to dictionary (tasks: {include_tasks}, sprints: {include_sprints}, metrics: {include_metrics})")
        
        # Parse technology stack from JSON string
        tech_stack = self._get_technology_list()

        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status.value,
            'repository_url': self.repository_url,
            'documentation_url': self.documentation_url,
            'technology_stack': tech_stack,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'estimated_hours': self.estimated_hours,
            'priority': self.priority,
            'budget': self.budget,
            'completion_percentage': self.completion_percentage,
            'client_name': self.client_name,
            'client_email': self.client_email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'owner': self.owner.to_dict() if self.owner else None,
            'tasks_count': len(self.tasks),
            'sprints_count': len(self.sprints),
            'team_members_count': len(self.team_members),
            'is_overdue': self.is_overdue(),
            'days_remaining': self.days_remaining()
        }
        
        if include_tasks:
            result['tasks'] = [task.to_dict() for task in self.tasks]
            
        if include_sprints:
            result['sprints'] = [sprint.to_dict() for sprint in self.sprints]
            
        if include_metrics:
            result['metrics'] = self.get_project_metrics()
            
        if include_team:
            result['team_members'] = [
                {
                    'user': member.user.to_dict() if member.user else None,
                    'role': member.role,
                    'joined_at': member.joined_at.isoformat() if hasattr(member, 'joined_at') and member.joined_at else None
                }
                for member in self.team_members
            ]
            result['active_sprint'] = self.get_active_sprint().to_dict() if self.get_active_sprint() else None
            
        return result

    def __repr__(self):
        return f'<Project {self.id}: {self.name} ({self.status.value})>'