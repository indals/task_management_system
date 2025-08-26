"""
Flask Application Factory

This module contains the application factory and extension initialization.
"""

import os
import time
from functools import wraps
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

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

def create_app(config_name='development'):
    """
    Application factory function.
    
    Args:
        config_name (str): Configuration environment ('development', 'production', 'testing')
        
    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration
    from app.config import get_config
    app.config.from_object(get_config(config_name))
    
    # Add database connection pooling configuration
    app.config.setdefault('SQLALCHEMY_ENGINE_OPTIONS', {
        'pool_pre_ping': True,      # Validates connections before use
        'pool_recycle': 300,        # Recycle connections every 5 minutes
        'pool_timeout': 20,         # Wait 20 seconds for connection
        'max_overflow': 0,          # Don't create extra connections
        'pool_size': 5,             # Number of connections to maintain
    })
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    }, supports_credentials=True)
    
    # Import models to ensure they are registered with SQLAlchemy
    # This is CRITICAL for Flask-Migrate to work properly
    try:
        from app import models  # This imports all models via models/__init__.py
        print("✅ Models imported successfully")
    except ImportError as e:
        print(f"⚠️  Warning: Could not import models: {e}")
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register health check routes
    register_health_routes(app)
    
    # Test database connection
    if config_name != 'testing':
        if not test_db_connection(app):
            print("⚠️  Warning: Database connection test failed")
    
    # Add request logging for development
    if config_name == 'development':
        @app.before_request
        def log_request_info():
            from flask import request
            print(f"🌐 {request.method} {request.url}")
    
    print(f"✅ Flask app created with {config_name} configuration")
    return app

def register_error_handlers(app):
    """Register global error handlers"""
    from app.utils.response import error_response, server_error_response, not_found_response
    
    @app.errorhandler(404)
    def not_found(error):
        return not_found_response("Resource not found")
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return server_error_response("Internal server error")
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle unexpected exceptions"""
        db.session.rollback()
        print(f"❌ Unhandled exception: {e}")
        if app.config.get('DEBUG'):
            raise e  # Re-raise in debug mode
        return server_error_response("An unexpected error occurred")

def register_health_routes(app):
    """Register health check routes"""
    @app.route('/health')
    def health_check():
        """General health check endpoint"""
        return {
            'status': 'healthy', 
            'service': 'task-management-api',
            'version': '1.0.0'
        }, 200
    
    @app.route('/health/db')
    def db_health_check():
        """Database health check endpoint"""
        try:
            with app.app_context():
                db.session.execute(db.text('SELECT 1'))
                return {
                    'status': 'healthy', 
                    'database': 'connected',
                    'engine': str(db.engine.url).split('@')[0] + '@***'
                }, 200
        except Exception as e:
            return {
                'status': 'unhealthy', 
                'database': 'disconnected',
                'error': str(e)
            }, 500
    
    @app.route('/health/ready')
    def readiness_check():
        """Kubernetes readiness probe endpoint"""
        try:
            # Check database connection
            with app.app_context():
                db.session.execute(db.text('SELECT 1'))
            
            return {
                'status': 'ready',
                'checks': {
                    'database': 'ok'
                }
            }, 200
        except Exception as e:
            return {
                'status': 'not_ready',
                'checks': {
                    'database': 'fail'
                },
                'error': str(e)
            }, 503