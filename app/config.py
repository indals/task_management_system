"""
Application Configuration

This module contains all configuration classes for different environments.
Configuration values are loaded from environment variables with sensible defaults.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration with default settings."""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000))  # 30 days
    
    # Database settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # File upload settings
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'app/static/uploads')
    
    # Email settings (for notifications)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@taskmanager.com')
    
    # Redis settings (for caching and background tasks)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Celery settings (for background tasks)
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # Security settings
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CORS settings
    CORS_HEADERS = 'Content-Type,Authorization'
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def init_app(app):
        """Initialize application with this config."""
        # Create upload directory if it doesn't exist
        upload_dir = app.config.get('UPLOAD_FOLDER')
        if upload_dir and not os.path.exists(upload_dir):
            os.makedirs(upload_dir, exist_ok=True)


class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    DEBUG = True
    FLASK_ENV = 'development'
    
    # Database - Use environment variable or default to local PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://myuser:ChangeMe123%21@localhost:5432/taskmanager_dev'
    )
    
    # Enable SQL query logging for debugging
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'false').lower() == 'true'
    
    # Development-specific settings
    WTF_CSRF_ENABLED = False  # Disable CSRF for API development
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        print("🔧 Development configuration loaded")


class ProductionConfig(Config):
    """Production environment configuration."""
    
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Database - Must be provided via environment variable
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@localhost:5432/taskmanager_prod'
    )
    
    # Production database settings
    SQLALCHEMY_ECHO = False  # Disable query logging in production
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0,
        'pool_size': 10,  # Higher pool size for production
    }
    
    # Security settings for production
    SESSION_COOKIE_SECURE = True  # Require HTTPS
    
    # Production logging
    LOG_TO_STDOUT = os.getenv('LOG_TO_STDOUT', 'true').lower() == 'true'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Configure logging for production
        if cls.LOG_TO_STDOUT:
            import logging
            from logging import StreamHandler
            
            file_handler = StreamHandler()
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
        
        print("🚀 Production configuration loaded")


class TestingConfig(Config):
    """Testing environment configuration."""
    
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'testing'
    
    # Use in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URL',
        'sqlite:///:memory:'
    )
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # Speed up password hashing for tests
    BCRYPT_LOG_ROUNDS = 4
    
    # Disable request rate limiting for tests
    RATELIMIT_ENABLED = False
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        print("🧪 Testing configuration loaded")


class DockerConfig(Config):
    """Docker environment configuration."""
    
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    
    # Docker-specific database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://taskmanager:taskmanager123@db:5432/taskmanager'
    )
    
    # Redis URL for Docker
    REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        print("🐳 Docker configuration loaded")


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """
    Get configuration class by name.
    
    Args:
        config_name (str): Name of configuration ('development', 'production', etc.)
        
    Returns:
        Config: Configuration class
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    return config.get(config_name, DevelopmentConfig)