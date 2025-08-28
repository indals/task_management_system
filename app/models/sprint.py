# app/models/sprint.py
from app import db
from datetime import datetime, timedelta
from .enums import SprintStatus

# Import logging and caching utilities
from app.utils.logger import get_logger, log_db_query
from app.utils.cache_utils import cache, cached_per_user, invalidate_user_cache, CacheKeys

# Initialize logger for this module
logger = get_logger('sprints')

class Sprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(SprintStatus), nullable=False, default=SprintStatus.PLANNED)
    
    # Project relationship
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    
    # Sprint duration
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    
    # Sprint goals and metrics
    goal = db.Column(db.Text)
    capacity_hours = db.Column(db.Float)
    velocity_points = db.Column(db.Integer)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', back_populates='sprints')
    tasks = db.relationship('Task', back_populates='sprint')

    @classmethod
    def create_sprint(cls, name, project_id, start_date, end_date, description=None, 
                     goal=None, capacity_hours=None, velocity_points=None):
        """Create a new sprint with validation, logging and cache management."""
        logger.info(f"Creating sprint '{name}' for project {project_id}")
        
        # Validation
        if not name or not name.strip():
            logger.warning(f"Sprint creation failed: Empty name for project {project_id}")
            raise ValueError("Sprint name cannot be empty")
        
        if start_date >= end_date:
            logger.warning(f"Sprint creation failed: Invalid date range for '{name}'")
            raise ValueError("Start date must be before end date")
        
        # Check for overlapping sprints in the same project
        overlapping = cls.query.filter(
            cls.project_id == project_id,
            cls.status.in_([SprintStatus.ACTIVE, SprintStatus.PLANNED]),
            cls.start_date < end_date,
            cls.end_date > start_date
        ).first()
        
        if overlapping:
            logger.warning(f"Sprint creation failed: Overlaps with sprint {overlapping.id}")
            raise ValueError(f"Sprint overlaps with existing sprint: {overlapping.name}")
        
        try:
            sprint = cls(
                name=name.strip(),
                description=description.strip() if description else None,
                project_id=project_id,
                start_date=start_date,
                end_date=end_date,
                goal=goal.strip() if goal else None,
                capacity_hours=capacity_hours,
                velocity_points=velocity_points
            )
            
            db.session.add(sprint)
            db.session.commit()
            
            logger.info(f"Sprint created successfully: ID {sprint.id} - '{name}'")
            
            # Invalidate related caches
            cls._invalidate_project_sprints_cache(project_id)
            cache.delete('active_sprints_list')
            
            # Log database query for monitoring
            log_db_query("Sprint", "CREATE", sprint.id)
            
            return sprint
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to create sprint '{name}': {str(e)}")
            raise

    def update_sprint(self, name=None, description=None, start_date=None, end_date=None,
                     goal=None, capacity_hours=None, velocity_points=None):
        """Update sprint with validation, logging and cache invalidation."""
        logger.info(f"Updating sprint {self.id}")
        
        changes = []
        
        # Validate date changes
        new_start = start_date if start_date is not None else self.start_date
        new_end = end_date if end_date is not None else self.end_date
        
        if new_start >= new_end:
            logger.warning(f"Sprint update failed: Invalid date range for sprint {self.id}")
            raise ValueError("Start date must be before end date")
        
        # Check for overlapping sprints if dates are changing
        if start_date is not None or end_date is not None:
            overlapping = Sprint.query.filter(
                Sprint.project_id == self.project_id,
                Sprint.id != self.id,
                Sprint.status.in_([SprintStatus.ACTIVE, SprintStatus.PLANNED]),
                Sprint.start_date < new_end,
                Sprint.end_date > new_start
            ).first()
            
            if overlapping:
                logger.warning(f"Sprint update failed: Would overlap with sprint {overlapping.id}")
                raise ValueError(f"Sprint would overlap with existing sprint: {overlapping.name}")
        
        # Track changes for logging
        if name is not None and name.strip() != self.name:
            changes.append(f"name: '{self.name}' -> '{name.strip()}'")
            self.name = name.strip()
        
        if description is not None and description != self.description:
            changes.append("description updated")
            self.description = description.strip() if description else None
        
        if start_date is not None and start_date != self.start_date:
            changes.append(f"start_date: {self.start_date} -> {start_date}")
            self.start_date = start_date
        
        if end_date is not None and end_date != self.end_date:
            changes.append(f"end_date: {self.end_date} -> {end_date}")
            self.end_date = end_date
        
        if goal is not None and goal != self.goal:
            changes.append("goal updated")
            self.goal = goal.strip() if goal else None
        
        if capacity_hours is not None and capacity_hours != self.capacity_hours:
            changes.append(f"capacity_hours: {capacity_hours}")
            self.capacity_hours = capacity_hours
        
        if velocity_points is not None and velocity_points != self.velocity_points:
            changes.append(f"velocity_points: {velocity_points}")
            self.velocity_points = velocity_points
        
        if changes:
            try:
                db.session.commit()
                logger.info(f"Sprint {self.id} updated: {', '.join(changes)}")
                
                # Invalidate related caches
                self._invalidate_sprint_caches()
                
                # Log database query for monitoring
                log_db_query("Sprint", "UPDATE", self.id)
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Failed to update sprint {self.id}: {str(e)}")
                raise
        else:
            logger.debug(f"No changes in sprint update for sprint {self.id}")

    def start_sprint(self):
        """Start the sprint with logging and cache management."""
        logger.info(f"Starting sprint {self.id}")
        
        if self.status != SprintStatus.PLANNED:
            logger.warning(f"Sprint start failed: Sprint {self.id} is not in PLANNED status")
            raise ValueError("Only planned sprints can be started")
        
        # Check if another sprint is already active in the same project
        active_sprint = Sprint.query.filter(
            Sprint.project_id == self.project_id,
            Sprint.status == SprintStatus.ACTIVE,
            Sprint.id != self.id
        ).first()
        
        if active_sprint:
            logger.warning(f"Sprint start failed: Sprint {active_sprint.id} is already active")
            raise ValueError(f"Another sprint is already active: {active_sprint.name}")
        
        try:
            self.status = SprintStatus.ACTIVE
            db.session.commit()
            
            logger.info(f"Sprint {self.id} started successfully")
            
            # Invalidate related caches
            self._invalidate_sprint_caches()
            cache.delete('active_sprints_list')
            
            # Log database query for monitoring
            log_db_query("Sprint", "START", self.id)
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to start sprint {self.id}: {str(e)}")
            raise

    def complete_sprint(self):
        """Complete the sprint with logging and cache management."""
        logger.info(f"Completing sprint {self.id}")
        
        if self.status != SprintStatus.ACTIVE:
            logger.warning(f"Sprint completion failed: Sprint {self.id} is not active")
            raise ValueError("Only active sprints can be completed")
        
        try:
            self.status = SprintStatus.COMPLETED
            db.session.commit()
            
            logger.info(f"Sprint {self.id} completed successfully")
            
            # Invalidate related caches
            self._invalidate_sprint_caches()
            cache.delete('active_sprints_list')
            
            # Log database query for monitoring
            log_db_query("Sprint", "COMPLETE", self.id)
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to complete sprint {self.id}: {str(e)}")
            raise

    def cancel_sprint(self):
        """Cancel the sprint with logging and cache management."""
        logger.info(f"Cancelling sprint {self.id}")
        
        if self.status == SprintStatus.COMPLETED:
            logger.warning(f"Sprint cancellation failed: Sprint {self.id} is already completed")
            raise ValueError("Cannot cancel a completed sprint")
        
        try:
            self.status = SprintStatus.CANCELLED
            db.session.commit()
            
            logger.info(f"Sprint {self.id} cancelled successfully")
            
            # Invalidate related caches
            self._invalidate_sprint_caches()
            cache.delete('active_sprints_list')
            
            # Log database query for monitoring
            log_db_query("Sprint", "CANCEL", self.id)
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to cancel sprint {self.id}: {str(e)}")
            raise

    @classmethod
    @cache.cached(timeout=300, key_prefix='project_sprints')
    def get_project_sprints(cls, project_id, status_filter=None, limit=None):
        """Get sprints for a project with caching and filtering."""
        logger.debug(f"Fetching sprints for project {project_id} (status: {status_filter})")
        
        query = cls.query.filter_by(project_id=project_id).order_by(cls.start_date.desc())
        
        if status_filter:
            if isinstance(status_filter, str):
                status_filter = SprintStatus(status_filter)
            query = query.filter_by(status=status_filter)
        
        if limit:
            query = query.limit(limit)
        
        sprints = query.all()
        logger.debug(f"Retrieved {len(sprints)} sprints for project {project_id}")
        
        # Log database query for monitoring
        log_db_query("Sprint", "SELECT", None, {"project_id": project_id, "count": len(sprints)})
        
        return sprints

    @classmethod
    @cache.cached(timeout=180, key_prefix='active_sprints_list')
    def get_active_sprints(cls):
        """Get all active sprints with caching."""
        logger.debug("Fetching all active sprints")
        
        sprints = cls.query.filter_by(status=SprintStatus.ACTIVE).all()
        logger.debug(f"Retrieved {len(sprints)} active sprints")
        
        # Log database query for monitoring
        log_db_query("Sprint", "SELECT", None, {"status": "ACTIVE", "count": len(sprints)})
        
        return sprints

    @cache.cached(timeout=300, key_prefix='sprint_metrics')
    def get_sprint_metrics(self):
        """Get comprehensive sprint metrics with caching."""
        logger.debug(f"Calculating metrics for sprint {self.id}")
        
        tasks = self.tasks
        total_tasks = len(tasks)
        
        if total_tasks == 0:
            return {
                'total_tasks': 0,
                'completed_tasks': 0,
                'completion_percentage': 0,
                'total_story_points': 0,
                'completed_story_points': 0,
                'remaining_story_points': 0,
                'story_points_completion': 0,
                'average_task_completion_time': 0
            }
        
        completed_tasks = [task for task in tasks if task.status.value == 'DONE']
        total_story_points = sum(task.story_points or 0 for task in tasks)
        completed_story_points = sum(task.story_points or 0 for task in completed_tasks)
        
        # Calculate average completion time for completed tasks
        completion_times = []
        for task in completed_tasks:
            if task.completed_at and task.created_at:
                duration = (task.completed_at - task.created_at).total_seconds() / 3600  # hours
                completion_times.append(duration)
        
        avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0
        
        metrics = {
            'total_tasks': total_tasks,
            'completed_tasks': len(completed_tasks),
            'completion_percentage': (len(completed_tasks) / total_tasks) * 100,
            'total_story_points': total_story_points,
            'completed_story_points': completed_story_points,
            'remaining_story_points': total_story_points - completed_story_points,
            'story_points_completion': (completed_story_points / total_story_points * 100) if total_story_points > 0 else 0,
            'average_task_completion_time': avg_completion_time
        }
        
        logger.debug(f"Sprint {self.id} metrics: {metrics['completion_percentage']:.1f}% complete")
        return metrics

    @cache.cached(timeout=600, key_prefix='sprint_burndown')
    def get_burndown_data(self):
        """Get burndown chart data for this sprint with caching."""
        logger.debug(f"Generating burndown data for sprint {self.id}")
        
        metrics = self.get_sprint_metrics()
        
        # Calculate daily burndown (simplified version)
        total_days = (self.end_date - self.start_date).days
        days_elapsed = min((datetime.utcnow() - self.start_date).days, total_days)
        days_remaining = max(total_days - days_elapsed, 0)
        
        # Ideal burndown line
        ideal_daily_burn = metrics['total_story_points'] / total_days if total_days > 0 else 0
        ideal_remaining = max(metrics['total_story_points'] - (ideal_daily_burn * days_elapsed), 0)
        
        burndown_data = {
            'total_points': metrics['total_story_points'],
            'completed_points': metrics['completed_story_points'],
            'remaining_points': metrics['remaining_story_points'],
            'ideal_remaining': ideal_remaining,
            'completion_percentage': metrics['completion_percentage'],
            'days_total': total_days,
            'days_elapsed': days_elapsed,
            'days_remaining': days_remaining,
            'velocity': metrics['completed_story_points'] / max(days_elapsed, 1) if days_elapsed > 0 else 0
        }
        
        logger.debug(f"Sprint {self.id} burndown: {burndown_data['remaining_points']} points remaining")
        return burndown_data

    def get_completion_percentage(self):
        """Calculate sprint completion based on tasks with caching consideration."""
        metrics = self.get_sprint_metrics()
        return metrics['completion_percentage']

    def get_total_story_points(self):
        """Get total story points for this sprint with caching consideration."""
        metrics = self.get_sprint_metrics()
        return metrics['total_story_points']

    def get_completed_story_points(self):
        """Get completed story points for this sprint with caching consideration."""
        metrics = self.get_sprint_metrics()
        return metrics['completed_story_points']

    def is_active(self):
        """Check if sprint is currently active with enhanced logic."""
        now = datetime.utcnow()
        is_currently_active = (
            self.status == SprintStatus.ACTIVE and 
            self.start_date <= now <= self.end_date
        )
        
        logger.debug(f"Sprint {self.id} active status: {is_currently_active}")
        return is_currently_active

    def is_overdue(self):
        """Check if active sprint is overdue."""
        now = datetime.utcnow()
        overdue = (self.status == SprintStatus.ACTIVE and now > self.end_date)
        
        if overdue:
            logger.info(f"Sprint {self.id} is overdue by {(now - self.end_date).days} days")
        
        return overdue

    def days_remaining(self):
        """Get number of days remaining in sprint with enhanced calculation."""
        if self.status != SprintStatus.ACTIVE:
            return 0
        
        now = datetime.utcnow()
        if now > self.end_date:
            return 0
        
        remaining = (self.end_date - now).days
        logger.debug(f"Sprint {self.id} has {remaining} days remaining")
        return remaining

    def hours_remaining(self):
        """Get number of hours remaining in sprint."""
        if self.status != SprintStatus.ACTIVE:
            return 0
        
        now = datetime.utcnow()
        if now > self.end_date:
            return 0
        
        remaining_hours = (self.end_date - now).total_seconds() / 3600
        return max(0, int(remaining_hours))

    @classmethod
    def _invalidate_project_sprints_cache(cls, project_id):
        """Helper method to invalidate project-related sprint caches."""
        logger.debug(f"Invalidating sprint caches for project {project_id}")
        cache.delete(f'project_sprints_{project_id}')

    def _invalidate_sprint_caches(self):
        """Helper method to invalidate all caches related to this sprint."""
        logger.debug(f"Invalidating all caches for sprint {self.id}")
        
        # Invalidate specific sprint caches
        cache.delete(f'sprint_metrics_{self.id}')
        cache.delete(f'sprint_burndown_{self.id}')
        
        # Invalidate project-related caches
        self._invalidate_project_sprints_cache(self.project_id)

    def can_be_edited(self):
        """Check if sprint can be edited based on status and timing."""
        can_edit = self.status in [SprintStatus.PLANNED, SprintStatus.ACTIVE]
        logger.debug(f"Sprint {self.id} edit permission: {can_edit}")
        return can_edit

    def can_be_started(self):
        """Check if sprint can be started."""
        can_start = (
            self.status == SprintStatus.PLANNED and 
            datetime.utcnow() >= self.start_date - timedelta(days=1)  # Allow starting 1 day early
        )
        logger.debug(f"Sprint {self.id} start permission: {can_start}")
        return can_start

    def can_be_completed(self):
        """Check if sprint can be completed."""
        can_complete = self.status == SprintStatus.ACTIVE
        logger.debug(f"Sprint {self.id} complete permission: {can_complete}")
        return can_complete

    def to_dict(self, include_tasks=False, include_metrics=False):
        """Convert sprint to dictionary with enhanced options and caching consideration."""
        logger.debug(f"Converting sprint {self.id} to dictionary (tasks: {include_tasks}, metrics: {include_metrics})")
        
        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status.value,
            'project_id': self.project_id,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'goal': self.goal,
            'capacity_hours': self.capacity_hours,
            'velocity_points': self.velocity_points,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'project': self.project.to_dict() if self.project else None,
            'tasks_count': len(self.tasks),
            'is_active': self.is_active(),
            'is_overdue': self.is_overdue(),
            'days_remaining': self.days_remaining(),
            'hours_remaining': self.hours_remaining(),
            'can_be_edited': self.can_be_edited(),
            'can_be_started': self.can_be_started(),
            'can_be_completed': self.can_be_completed()
        }
        
        if include_tasks:
            result['tasks'] = [task.to_dict() for task in self.tasks]
        
        if include_metrics:
            result['metrics'] = self.get_sprint_metrics()
            result['burndown_data'] = self.get_burndown_data()
            
        return result

    def __repr__(self):
        return f'<Sprint {self.id}: {self.name} ({self.status.value})>'