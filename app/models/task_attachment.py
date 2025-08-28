# app/models/task_attachment.py
from app import db
from datetime import datetime
import os
import mimetypes
from pathlib import Path

# Import logging and caching utilities
from app.utils.logger import get_logger, log_db_query
from app.utils.cache_utils import cache, cached_per_user, invalidate_user_cache, CacheKeys

# Initialize logger for this module
logger = get_logger('task_attachments')

class TaskAttachment(db.Model):
    __tablename__ = 'task_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'), nullable=False)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    # File information
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)  # Size in bytes
    mime_type = db.Column(db.String(100))
    
    # Additional metadata
    description = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=True)
    download_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_accessed_at = db.Column(db.DateTime)

    # Relationships
    task = db.relationship('Task', back_populates='attachments')
    uploaded_by = db.relationship('User', backref='uploaded_attachments')

    @classmethod
    def upload_attachment(cls, task_id, uploaded_by_id, file_obj, original_filename, 
                         description=None, is_public=True, upload_dir='uploads/tasks'):
        """Upload and create a new task attachment with comprehensive logging."""
        logger.info(f"Uploading attachment '{original_filename}' for task {task_id} by user {uploaded_by_id}")
        
        # Validation
        if not original_filename or not original_filename.strip():
            logger.warning(f"Attachment upload failed: Empty filename for task {task_id}")
            raise ValueError("Filename cannot be empty")
        
        # Check file size (example: 10MB limit)
        max_size = 10 * 1024 * 1024  # 10MB
        file_obj.seek(0, os.SEEK_END)
        file_size = file_obj.tell()
        file_obj.seek(0)  # Reset file pointer
        
        if file_size > max_size:
            logger.warning(f"Attachment upload failed: File too large ({file_size} bytes) for task {task_id}")
            raise ValueError(f"File size ({cls._format_file_size(file_size)}) exceeds maximum allowed size (10MB)")
        
        if file_size == 0:
            logger.warning(f"Attachment upload failed: Empty file for task {task_id}")
            raise ValueError("Cannot upload empty file")
        
        # Generate secure filename
        file_extension = Path(original_filename).suffix.lower()
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        secure_filename = f"task_{task_id}_{timestamp}_{uploaded_by_id}{file_extension}"
        
        # Ensure upload directory exists
        upload_path = Path(upload_dir)
        upload_path.mkdir(parents=True, exist_ok=True)
        
        full_file_path = upload_path / secure_filename
        
        # Detect MIME type
        mime_type = mimetypes.guess_type(original_filename)[0] or 'application/octet-stream'
        
        try:
            # Save file to disk
            with open(full_file_path, 'wb') as f:
                f.write(file_obj.read())
            
            # Create database record
            attachment = cls(
                task_id=task_id,
                uploaded_by_id=uploaded_by_id,
                filename=secure_filename,
                original_filename=original_filename.strip(),
                file_path=str(full_file_path),
                file_size=file_size,
                mime_type=mime_type,
                description=description.strip() if description else None,
                is_public=is_public
            )
            
            db.session.add(attachment)
            db.session.commit()
            
            logger.info(f"Attachment uploaded successfully: ID {attachment.id} - '{original_filename}' ({cls._format_file_size(file_size)})")
            
            # Invalidate related caches
            cls._invalidate_task_attachments_cache(task_id)
            invalidate_user_cache(uploaded_by_id, CacheKeys.USER_ATTACHMENTS)
            cache.delete('recent_attachments')
            
            # Log database query for monitoring
            log_db_query("TaskAttachment", "CREATE", attachment.id, {
                "file_size": file_size,
                "mime_type": mime_type,
                "task_id": task_id
            })
            
            return attachment
            
        except Exception as e:
            # Clean up file if database operation failed
            if full_file_path.exists():
                try:
                    full_file_path.unlink()
                except Exception as cleanup_error:
                    logger.error(f"Failed to cleanup file after database error: {cleanup_error}")
            
            db.session.rollback()
            logger.error(f"Failed to upload attachment '{original_filename}' for task {task_id}: {str(e)}")
            raise

    def update_metadata(self, description=None, is_public=None):
        """Update attachment metadata with logging."""
        logger.info(f"Updating metadata for attachment {self.id}")
        
        changes = []
        
        if description is not None and description != self.description:
            changes.append("description updated")
            self.description = description.strip() if description else None
        
        if is_public is not None and is_public != self.is_public:
            changes.append(f"is_public: {is_public}")
            self.is_public = is_public
        
        if changes:
            try:
                db.session.commit()
                logger.info(f"Attachment {self.id} metadata updated: {', '.join(changes)}")
                
                # Invalidate related caches
                self._invalidate_attachment_caches()
                
                # Log database query for monitoring
                log_db_query("TaskAttachment", "UPDATE", self.id)
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Failed to update attachment {self.id} metadata: {str(e)}")
                raise
        else:
            logger.debug(f"No changes in metadata update for attachment {self.id}")

    def delete_attachment(self):
        """Delete attachment with file cleanup and comprehensive logging."""
        logger.info(f"Deleting attachment {self.id} - '{self.original_filename}'")
        
        attachment_id = self.id
        task_id = self.task_id
        uploaded_by_id = self.uploaded_by_id
        file_path = self.file_path
        original_filename = self.original_filename
        
        try:
            # Remove database record first
            db.session.delete(self)
            db.session.commit()
            
            # Then try to delete the physical file
            file_deleted = self._delete_physical_file(file_path)
            
            if file_deleted:
                logger.info(f"Attachment {attachment_id} and file deleted successfully")
            else:
                logger.warning(f"Attachment {attachment_id} deleted from database, but file cleanup failed")
            
            # Invalidate related caches
            self._invalidate_task_attachments_cache(task_id)
            invalidate_user_cache(uploaded_by_id, CacheKeys.USER_ATTACHMENTS)
            cache.delete('recent_attachments')
            
            # Log database query for monitoring
            log_db_query("TaskAttachment", "DELETE", attachment_id, {
                "filename": original_filename,
                "file_deleted": file_deleted
            })
            
            return file_deleted
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to delete attachment {attachment_id}: {str(e)}")
            raise

    def record_download(self, downloaded_by_user_id=None):
        """Record a download event with logging."""
        logger.debug(f"Recording download for attachment {self.id}")
        
        try:
            self.download_count += 1
            self.last_accessed_at = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"Download recorded for attachment {self.id} (count: {self.download_count})")
            
            # Invalidate attachment cache to refresh download count
            self._invalidate_attachment_caches()
            
            # Log database query for monitoring
            log_db_query("TaskAttachment", "DOWNLOAD", self.id, {
                "download_count": self.download_count,
                "downloaded_by": downloaded_by_user_id
            })
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to record download for attachment {self.id}: {str(e)}")

    @classmethod
    @cache.cached(timeout=300, key_prefix='task_attachments')
    def get_task_attachments(cls, task_id, include_private=True):
        """Get attachments for a specific task with caching."""
        logger.debug(f"Fetching attachments for task {task_id}")
        
        query = cls.query.filter_by(task_id=task_id).order_by(cls.uploaded_at.desc())
        
        if not include_private:
            query = query.filter_by(is_public=True)
        
        attachments = query.all()
        logger.debug(f"Retrieved {len(attachments)} attachments for task {task_id}")
        
        # Log database query for monitoring
        log_db_query("TaskAttachment", "SELECT", None, {"task_id": task_id, "count": len(attachments)})
        
        return attachments

    @cached_per_user(timeout=300, key_prefix=CacheKeys.USER_ATTACHMENTS)
    def get_user_attachments(self, limit=None):
        """Get attachments uploaded by a specific user with caching."""
        logger.debug(f"Fetching attachments uploaded by user {self.uploaded_by_id}")
        
        query = TaskAttachment.query.filter_by(uploaded_by_id=self.uploaded_by_id).order_by(TaskAttachment.uploaded_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        attachments = query.all()
        logger.debug(f"Retrieved {len(attachments)} attachments uploaded by user {self.uploaded_by_id}")
        
        # Log database query for monitoring
        log_db_query("TaskAttachment", "SELECT", None, {"uploaded_by_id": self.uploaded_by_id, "count": len(attachments)})
        
        return attachments

    @classmethod
    @cache.cached(timeout=180, key_prefix='recent_attachments')
    def get_recent_attachments(cls, limit=10):
        """Get recent attachments across all tasks with caching."""
        logger.debug(f"Fetching {limit} recent attachments")
        
        attachments = cls.query.filter_by(is_public=True).order_by(cls.uploaded_at.desc()).limit(limit).all()
        logger.debug(f"Retrieved {len(attachments)} recent attachments")
        
        # Log database query for monitoring
        log_db_query("TaskAttachment", "SELECT", None, {"recent_limit": limit, "count": len(attachments)})
        
        return attachments

    @classmethod
    def get_storage_statistics(cls):
        """Get storage usage statistics with caching."""
        cache_key = 'attachment_storage_stats'
        cached_stats = cache.get(cache_key)
        
        if cached_stats:
            logger.debug("Retrieved storage statistics from cache")
            return cached_stats
        
        logger.debug("Calculating storage statistics")
        
        # Calculate statistics
        total_files = cls.query.count()
        total_size = db.session.query(db.func.sum(cls.file_size)).scalar() or 0
        
        # Get file type breakdown
        file_types = db.session.query(
            cls.mime_type,
            db.func.count(cls.id).label('count'),
            db.func.sum(cls.file_size).label('total_size')
        ).group_by(cls.mime_type).all()
        
        type_breakdown = [
            {
                'mime_type': ft.mime_type,
                'count': ft.count,
                'total_size': ft.total_size or 0,
                'formatted_size': cls._format_file_size(ft.total_size or 0)
            }
            for ft in file_types
        ]
        
        stats = {
            'total_files': total_files,
            'total_size_bytes': total_size,
            'total_size_formatted': cls._format_file_size(total_size),
            'average_file_size': total_size / total_files if total_files > 0 else 0,
            'file_type_breakdown': type_breakdown
        }
        
        # Cache for 30 minutes
        cache.set(cache_key, stats, timeout=1800)
        
        logger.info(f"Storage statistics: {total_files} files, {cls._format_file_size(total_size)} total")
        
        # Log database query for monitoring
        log_db_query("TaskAttachment", "STATS", None, stats)
        
        return stats

    @classmethod
    def search_attachments(cls, search_term, task_id=None, file_type=None, uploaded_by_id=None, limit=None):
        """Search attachments by filename or description."""
        logger.info(f"Searching attachments with term: '{search_term}'")
        
        if not search_term or len(search_term.strip()) < 2:
            logger.warning("Search term too short or empty")
            return []
        
        query = cls.query.filter(
            db.or_(
                cls.original_filename.ilike(f'%{search_term}%'),
                cls.description.ilike(f'%{search_term}%')
            )
        ).filter_by(is_public=True)
        
        if task_id:
            query = query.filter_by(task_id=task_id)
        if uploaded_by_id:
            query = query.filter_by(uploaded_by_id=uploaded_by_id)
        if file_type:
            query = query.filter(cls.mime_type.ilike(f'{file_type}%'))
        
        query = query.order_by(cls.uploaded_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        attachments = query.all()
        logger.info(f"Search returned {len(attachments)} attachments for term: '{search_term}'")
        
        # Log database query for monitoring
        log_db_query("TaskAttachment", "SEARCH", None, {
            "search_term": search_term,
            "task_id": task_id,
            "file_type": file_type,
            "count": len(attachments)
        })
        
        return attachments

    @staticmethod
    def _delete_physical_file(file_path):
        """Delete the physical file from storage with logging."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.debug(f"Physical file deleted: {file_path}")
                return True
            else:
                logger.warning(f"Physical file not found: {file_path}")
                return False
        except Exception as e:
            logger.error(f"Error deleting physical file {file_path}: {e}")
            return False

    def delete_file(self):
        """Delete the physical file from storage (legacy method)."""
        logger.warning(f"Using deprecated delete_file method for attachment {self.id}")
        return self._delete_physical_file(self.file_path)

    @staticmethod
    def _format_file_size(size_bytes):
        """Return human-readable file size."""
        if not size_bytes:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def get_formatted_file_size(self):
        """Return human-readable file size."""
        return self._format_file_size(self.file_size)

    def get_file_extension(self):
        """Get file extension from filename with logging."""
        extension = os.path.splitext(self.original_filename)[1].lower()
        logger.debug(f"File extension for attachment {self.id}: {extension}")
        return extension

    def get_file_category(self):
        """Get file category based on extension and MIME type."""
        extension = self.get_file_extension()
        mime_type = self.mime_type or ''
        
        if self.is_image():
            return 'image'
        elif self.is_document():
            return 'document'
        elif self.is_code_file():
            return 'code'
        elif self.is_archive():
            return 'archive'
        elif self.is_video():
            return 'video'
        elif self.is_audio():
            return 'audio'
        else:
            return 'other'

    def is_image(self):
        """Check if attachment is an image."""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff']
        return (self.get_file_extension() in image_extensions or 
                (self.mime_type and self.mime_type.startswith('image/')))

    def is_document(self):
        """Check if attachment is a document."""
        doc_extensions = ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.ods', '.odp', '.xls', '.xlsx', '.ppt', '.pptx']
        return (self.get_file_extension() in doc_extensions or
                (self.mime_type and any(doc_type in self.mime_type for doc_type in 
                ['pdf', 'document', 'text', 'spreadsheet', 'presentation'])))

    def is_code_file(self):
        """Check if attachment is a code file."""
        code_extensions = ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go', '.rs', 
                          '.ts', '.jsx', '.vue', '.sql', '.json', '.xml', '.yaml', '.yml', '.md', '.sh', 
                          '.bat', '.ps1', '.r', '.scala', '.kt', '.swift', '.dart']
        return self.get_file_extension() in code_extensions

    def is_archive(self):
        """Check if attachment is an archive file."""
        archive_extensions = ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz']
        return self.get_file_extension() in archive_extensions

    def is_video(self):
        """Check if attachment is a video file."""
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v']
        return (self.get_file_extension() in video_extensions or
                (self.mime_type and self.mime_type.startswith('video/')))

    def is_audio(self):
        """Check if attachment is an audio file."""
        audio_extensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a']
        return (self.get_file_extension() in audio_extensions or
                (self.mime_type and self.mime_type.startswith('audio/')))

    def is_safe_for_preview(self):
        """Check if file is safe to preview in browser."""
        safe_types = ['image', 'document']
        safe_extensions = ['.txt', '.md', '.json', '.xml', '.csv']
        
        return (self.get_file_category() in safe_types or 
                self.get_file_extension() in safe_extensions or
                (self.mime_type and self.mime_type.startswith('text/')))

    def can_be_edited_by(self, user):
        """Check if user can edit this attachment."""
        can_edit = (
            self.uploaded_by_id == user.id or 
            user.role.value in ['ADMIN', 'MANAGER']
        )
        logger.debug(f"Attachment {self.id} edit permission for user {user.id}: {can_edit}")
        return can_edit

    def can_be_deleted_by(self, user):
        """Check if user can delete this attachment."""
        can_delete = (
            self.uploaded_by_id == user.id or 
            user.role.value in ['ADMIN', 'MANAGER']
        )
        logger.debug(f"Attachment {self.id} delete permission for user {user.id}: {can_delete}")
        return can_delete

    @classmethod
    def _invalidate_task_attachments_cache(cls, task_id):
        """Helper method to invalidate task-related attachment caches."""
        logger.debug(f"Invalidating attachment caches for task {task_id}")
        cache.delete(f'task_attachments_{task_id}')

    def _invalidate_attachment_caches(self):
        """Helper method to invalidate all caches related to this attachment."""
        logger.debug(f"Invalidating all caches for attachment {self.id}")
        
        # Invalidate task-specific caches
        self._invalidate_task_attachments_cache(self.task_id)
        
        # Invalidate user-specific caches
        invalidate_user_cache(self.uploaded_by_id, CacheKeys.USER_ATTACHMENTS)
        
        # Invalidate global caches
        cache.delete('recent_attachments')
        cache.delete('attachment_storage_stats')

    def get_age_in_hours(self):
        """Get attachment age in hours."""
        age_hours = int((datetime.utcnow() - self.uploaded_at).total_seconds() / 3600)
        return max(0, age_hours)

    def is_recent(self, hours=24):
        """Check if attachment was uploaded within specified hours."""
        return self.get_age_in_hours() <= hours

    def to_dict(self, include_user_details=True, include_stats=False):
        """Convert attachment to dictionary with enhanced options and caching consideration."""
        logger.debug(f"Converting attachment {self.id} to dictionary")
        
        result = {
            'id': self.id,
            'task_id': self.task_id,
            'uploaded_by_id': self.uploaded_by_id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'description': self.description,
            'is_public': self.is_public,
            'download_count': self.download_count,
            'uploaded_at': self.uploaded_at.isoformat(),
            'last_accessed_at': self.last_accessed_at.isoformat() if self.last_accessed_at else None,
            'file_size_formatted': self.get_formatted_file_size(),
            'file_extension': self.get_file_extension(),
            'file_category': self.get_file_category(),
            'is_image': self.is_image(),
            'is_document': self.is_document(),
            'is_code_file': self.is_code_file(),
            'is_safe_for_preview': self.is_safe_for_preview(),
            'age_hours': self.get_age_in_hours(),
            'is_recent': self.is_recent()
        }
        
        if include_user_details and self.uploaded_by:
            result['uploaded_by'] = {
                'id': self.uploaded_by.id,
                'name': self.uploaded_by.name,
                'avatar_url': self.uploaded_by.avatar_url,
                'role': self.uploaded_by.role.value
            }
        
        if include_stats:
            result['download_stats'] = {
                'total_downloads': self.download_count,
                'last_accessed': self.last_accessed_at.isoformat() if self.last_accessed_at else None
            }
        
        return result

    def __repr__(self):
        return f'<TaskAttachment {self.id}: {self.original_filename} for Task {self.task_id}>'