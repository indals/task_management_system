# app/models/task_comment.py
from app import db
from datetime import datetime

# Import logging and caching utilities
from app.utils.logger import get_logger, log_db_query
from app.utils.cache_utils import cache, cached_per_user, invalidate_user_cache, CacheKeys

# Initialize logger for this module
logger = get_logger('task_comments')

class TaskComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    task = db.relationship('Task', back_populates='comments')
    user = db.relationship('User', back_populates='task_comments')

    @classmethod
    def create_comment(cls, task_id, user_id, comment_text):
        """Create a new task comment with logging and cache management."""
        logger.info(f"Creating comment for task {task_id} by user {user_id}")
        
        if not comment_text or not comment_text.strip():
            logger.warning(f"Comment creation failed: Empty comment text for task {task_id}")
            raise ValueError("Comment text cannot be empty")
        
        try:
            comment = cls(
                task_id=task_id,
                user_id=user_id,
                comment=comment_text.strip()
            )
            
            db.session.add(comment)
            db.session.commit()
            
            logger.info(f"Comment created successfully: ID {comment.id} for task {task_id}")
            
            # Invalidate related caches
            cls._invalidate_task_comments_cache(task_id)
            invalidate_user_cache(user_id, CacheKeys.USER_COMMENTS)
            
            # Log database query for monitoring
            log_db_query("TaskComment", "CREATE", comment.id)
            
            return comment
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to create comment for task {task_id}: {str(e)}")
            raise

    def update_comment(self, new_comment_text):
        """Update comment text with logging and cache invalidation."""
        logger.info(f"Updating comment {self.id}")
        
        if not new_comment_text or not new_comment_text.strip():
            logger.warning(f"Comment update failed: Empty comment text for comment {self.id}")
            raise ValueError("Comment text cannot be empty")
        
        old_comment = self.comment
        self.comment = new_comment_text.strip()
        
        try:
            db.session.commit()
            logger.info(f"Comment {self.id} updated successfully")
            
            # Invalidate related caches
            self._invalidate_task_comments_cache(self.task_id)
            invalidate_user_cache(self.user_id, CacheKeys.USER_COMMENTS)
            
            # Log database query for monitoring
            log_db_query("TaskComment", "UPDATE", self.id)
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to update comment {self.id}: {str(e)}")
            # Revert the comment text
            self.comment = old_comment
            raise

    def delete_comment(self):
        """Delete comment with logging and cache cleanup."""
        logger.info(f"Deleting comment {self.id} from task {self.task_id}")
        
        comment_id = self.id
        task_id = self.task_id
        user_id = self.user_id
        
        try:
            db.session.delete(self)
            db.session.commit()
            
            logger.info(f"Comment {comment_id} deleted successfully")
            
            # Invalidate related caches
            self._invalidate_task_comments_cache(task_id)
            invalidate_user_cache(user_id, CacheKeys.USER_COMMENTS)
            
            # Log database query for monitoring
            log_db_query("TaskComment", "DELETE", comment_id)
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to delete comment {comment_id}: {str(e)}")
            raise

    @classmethod
    @cache.cached(timeout=300, key_prefix='task_comments')
    def get_task_comments(cls, task_id, limit=None, offset=None):
        """Get comments for a specific task with caching and pagination."""
        logger.debug(f"Fetching comments for task {task_id} (limit: {limit}, offset: {offset})")
        
        query = cls.query.filter_by(task_id=task_id).order_by(cls.created_at.desc())
        
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        
        comments = query.all()
        logger.debug(f"Retrieved {len(comments)} comments for task {task_id}")
        
        # Log database query for monitoring
        log_db_query("TaskComment", "SELECT", None, {"task_id": task_id, "count": len(comments)})
        
        return comments

    @classmethod
    @cache.cached(timeout=180, key_prefix='task_comment_count')
    def get_task_comment_count(cls, task_id):
        """Get total comment count for a task with caching."""
        logger.debug(f"Counting comments for task {task_id}")
        
        count = cls.query.filter_by(task_id=task_id).count()
        logger.debug(f"Task {task_id} has {count} comments")
        
        # Log database query for monitoring
        log_db_query("TaskComment", "COUNT", None, {"task_id": task_id, "count": count})
        
        return count

    @cached_per_user(timeout=300, key_prefix=CacheKeys.USER_COMMENTS)
    def get_user_comments(self, limit=None):
        """Get comments by a specific user with caching."""
        logger.debug(f"Fetching comments by user {self.user_id} (limit: {limit})")
        
        query = TaskComment.query.filter_by(user_id=self.user_id).order_by(TaskComment.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        comments = query.all()
        logger.debug(f"Retrieved {len(comments)} comments by user {self.user_id}")
        
        # Log database query for monitoring
        log_db_query("TaskComment", "SELECT", None, {"user_id": self.user_id, "count": len(comments)})
        
        return comments

    @classmethod
    def get_recent_comments(cls, limit=10):
        """Get recent comments across all tasks with optional caching."""
        cache_key = f'recent_comments_{limit}'
        cached_result = cache.get(cache_key)
        
        if cached_result:
            logger.debug(f"Retrieved {limit} recent comments from cache")
            return cached_result
        
        logger.debug(f"Fetching {limit} recent comments from database")
        
        comments = cls.query.order_by(cls.created_at.desc()).limit(limit).all()
        
        # Cache for 5 minutes
        cache.set(cache_key, comments, timeout=300)
        
        logger.debug(f"Retrieved and cached {len(comments)} recent comments")
        
        # Log database query for monitoring
        log_db_query("TaskComment", "SELECT", None, {"recent_limit": limit, "count": len(comments)})
        
        return comments

    @classmethod
    def search_comments(cls, search_term, task_id=None, user_id=None, limit=None):
        """Search comments by text with optional filtering and logging."""
        logger.info(f"Searching comments with term: '{search_term}' (task_id: {task_id}, user_id: {user_id})")
        
        if not search_term or len(search_term.strip()) < 2:
            logger.warning("Search term too short or empty")
            return []
        
        query = cls.query.filter(cls.comment.ilike(f'%{search_term}%'))
        
        if task_id:
            query = query.filter_by(task_id=task_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        query = query.order_by(cls.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        comments = query.all()
        logger.info(f"Search returned {len(comments)} comments for term: '{search_term}'")
        
        # Log database query for monitoring
        log_db_query("TaskComment", "SEARCH", None, {
            "search_term": search_term,
            "task_id": task_id,
            "user_id": user_id,
            "count": len(comments)
        })
        
        return comments

    @classmethod
    def _invalidate_task_comments_cache(cls, task_id):
        """Helper method to invalidate task-related comment caches."""
        logger.debug(f"Invalidating comment caches for task {task_id}")
        
        # Invalidate specific caches
        cache.delete(f'task_comments_{task_id}')
        cache.delete(f'task_comment_count_{task_id}')
        
        # Invalidate recent comments cache
        for limit in [5, 10, 20, 50]:  # Common limits used
            cache.delete(f'recent_comments_{limit}')

    def can_edit(self, current_user):
        """Check if current user can edit this comment."""
        can_edit = (
            self.user_id == current_user.id or 
            current_user.role.value in ['ADMIN', 'MANAGER']
        )
        
        logger.debug(f"Comment {self.id} edit permission for user {current_user.id}: {can_edit}")
        return can_edit

    def can_delete(self, current_user):
        """Check if current user can delete this comment."""
        can_delete = (
            self.user_id == current_user.id or 
            current_user.role.value in ['ADMIN', 'MANAGER']
        )
        
        logger.debug(f"Comment {self.id} delete permission for user {current_user.id}: {can_delete}")
        return can_delete

    def get_age_in_minutes(self):
        """Get comment age in minutes for UI display."""
        age_minutes = int((datetime.utcnow() - self.created_at).total_seconds() / 60)
        return max(0, age_minutes)

    def is_recent(self, minutes=30):
        """Check if comment was created within specified minutes."""
        return self.get_age_in_minutes() <= minutes

    def to_dict(self, include_user_details=True):
        """Convert comment to dictionary with enhanced options and caching consideration."""
        logger.debug(f"Converting comment {self.id} to dictionary")
        
        result = {
            'id': self.id,
            'task_id': self.task_id,
            'user_id': self.user_id,
            'comment': self.comment,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'age_minutes': self.get_age_in_minutes(),
            'is_recent': self.is_recent()
        }
        
        if include_user_details and self.user:
            result['user'] = {
                'id': self.user.id,
                'name': self.user.name,
                'avatar_url': self.user.avatar_url,
                'role': self.user.role.value
            }
        
        return result

    def __repr__(self):
        return f'<TaskComment {self.id}: Task {self.task_id} by User {self.user_id}>'