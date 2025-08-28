"""
Caching utilities for the Task Management System
"""
from flask_caching import Cache
from functools import wraps
from flask_jwt_extended import get_jwt_identity
import json
import hashlib

# Initialize cache (will be configured in __init__.py)
cache = Cache()

def init_cache(app):
    """Initialize caching with the Flask app"""
    cache.init_app(app)
    return cache

# Cache key generators
def make_cache_key(*args, **kwargs):
    """Generate cache key from arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
    key_string = "|".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()

def user_cache_key(prefix="", **kwargs):
    """Generate cache key with current user"""
    user_id = get_jwt_identity() or 'anonymous'
    base_key = f"{prefix}:user_{user_id}"
    if kwargs:
        params = "|".join([f"{k}={v}" for k, v in sorted(kwargs.items())])
        base_key += f":{hashlib.md5(params.encode()).hexdigest()}"
    return base_key

# Custom cache decorators
def cached_per_user(timeout=300, key_prefix=""):
    """Cache decorator that includes user_id in key"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = user_cache_key(key_prefix or f.__name__, **kwargs)
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = f(*args, **kwargs)
            cache.set(cache_key, result, timeout=timeout)
            return result
        return decorated_function
    return decorator

def invalidate_user_cache(user_id, pattern="*"):
    """Invalidate all cache entries for a user"""
    try:
        # This requires Redis backend
        keys = cache.cache._read_clients.keys(f"*user_{user_id}*{pattern}*")
        if keys:
            cache.cache._write_client.delete(*keys)
            print(f"🗑️ Invalidated {len(keys)} cache entries for user {user_id}")
    except Exception as e:
        print(f"⚠️ Cache invalidation failed: {e}")

def invalidate_project_cache(project_id):
    """Invalidate all cache entries related to a project"""
    try:
        keys = cache.cache._read_clients.keys(f"*project_{project_id}*")
        if keys:
            cache.cache._write_client.delete(*keys)
            print(f"🗑️ Invalidated {len(keys)} cache entries for project {project_id}")
    except Exception as e:
        print(f"⚠️ Cache invalidation failed: {e}")

# Common cache patterns
class CacheKeys:
    USER_TASKS = "user_tasks"
    USER_PROJECTS = "user_projects" 
    PROJECT_TASKS = "project_tasks"
    PROJECT_MEMBERS = "project_members"
    SPRINT_TASKS = "sprint_tasks"
    USER_NOTIFICATIONS = "user_notifications"
    DASHBOARD_DATA = "dashboard_data"
    ANALYTICS_DATA = "analytics_data"