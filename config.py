class Config:
    """Base configuration with default settings."""
    SECRET_KEY = "your_secret_key"
    JWT_SECRET_KEY = "your_jwt_secret_key"
    FLASK_ENV = "development"
    FLASK_DEBUG = True
    CORS_HEADERS = 'Content-Type'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy track modifications

    @staticmethod
    def get_config(config_name):
        """Return the appropriate configuration class."""
        configs = {
            'production': ProductionConfig,
            'development': DevelopmentConfig,
            'testing': TestingConfig
        }
        return configs.get(config_name, DevelopmentConfig)  # Default to development


class DevelopmentConfig(Config):
    """Development environment settings."""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Enables SQL query logging for debugging
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:VGbtoCXHgBeOUzXmFxIULvZfZbwXqnDM@hopper.proxy.rlwy.net:20422/railway'


class ProductionConfig(Config):
    """Production environment settings."""
    DEBUG = False
    SQLALCHEMY_ECHO = False  # Disable query logging in production
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@production-db/dbname'


class TestingConfig(Config):
    """Testing environment settings."""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory DB for tests
