


from .base import BaseConfig


class DevelopmentConfig(BaseConfig):
    """Development environment settings."""

    DEBUG = False
    SQLALCHEMY_ECHO = False # Enables SQL query logging for debugging

    SQLALCHEMY_DATABASE_URI = 'postgresql://myuser:MySecurePassword123%21@dev-database.c1qe2o6s6oix.ap-south-1.rds.amazonaws.com:5432/myapp?sslmode=require'