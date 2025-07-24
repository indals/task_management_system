# app/__init__.py
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
import os
import time
from functools import wraps

# Initialize extensions globally
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def retry_db_operation(retries=3, delay=1):
    """Decorator to retry database operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries - 1:  # Last attempt
                        raise e
                    print(f"Database operation failed (attempt {attempt + 1}/{retries}): {e}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def test_db_connection(app):
    """Test if database connection is working"""
    try:
        with app.app_context():
            # Try to execute a simple query
            db.session.execute(db.text('SELECT 1'))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def create_app(config_name):
    """Factory function to create and configure the Flask app."""
    from flask import Flask
    from config import Config

    # Initialize the Flask app
    app = Flask(__name__)
    app.config.from_object(Config.get_config(config_name))

    # Add database connection pooling configuration
    app.config.setdefault('SQLALCHEMY_ENGINE_OPTIONS', {
        'pool_pre_ping': True,      # Validates connections before use
        'pool_recycle': 300,        # Recycle connections every 5 minutes
        'pool_timeout': 20,         # Wait 20 seconds for connection
        'max_overflow': 0,          # Don't create extra connections
        'pool_size': 5,             # Number of connections to maintain
    })

    # Enable CORS globally
    # CORS(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    from app.models.notification import Notification
    # Initialize extensions with the app
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Import models here to ensure they are registered with SQLAlchemy
    # This is CRITICAL for Flask-Migrate to work properly
    try:
        from app import models  # Import your models module
        print("✅ Models imported successfully")
    except ImportError as e:
        print(f"⚠️  Warning: Could not import models: {e}")
        # If you have models in different files, import them individually:
        # from app.models.user import User
        # from app.models.task import Task
        # etc.

    # Test database connection
    if not test_db_connection(app):
        print("⚠️  Warning: Database connection test failed")

    # Add database health check route
    @app.route('/api/health/db')
    def db_health_check():
        """Health check endpoint for database"""
        try:
            db.session.execute(db.text('SELECT 1'))
            return {'status': 'healthy', 'database': 'connected'}, 200
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}, 500

    @app.route('/api/health')
    def health_check():
        """General health check endpoint"""
        return {'status': 'healthy', 'service': 'task-management-api'}, 200

    return app