import os
from pathlib import Path

class BaseConfig:
    """Base configuration with common settings"""
    
    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent.absolute()
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    
    # Database settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # CORS settings
    CORS_HEADERS = 'Content-Type,Authorization'
    
    @classmethod
    def init_app(cls, app):
        """Initialize application with this config"""
        pass