"""
Flask Application Factory
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate


# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_class):
    """Create Flask application instance"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    config_class.init_app(app)
    
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
    })
    
    # Initialize Socket.IO if enabled
    # NEW - Import from utils instead of services
    from app.utils.socket_utils import init_socketio
    socketio = init_socketio(app)
    app.socketio = socketio
    
    # Import and register models
    from app import models
    
    # Register blueprints
    from app.routes import register_blueprints
    register_blueprints(app)
    print("\n🔍 Registered Routes:")
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            methods = ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            print(f"  {methods:15} {rule.rule}")
    print()
    
    
    # Register basic error handlers inline (temporary)
    register_basic_error_handlers(app)
    
    return app

def register_basic_error_handlers(app):
    """Register basic error handlers inline"""
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle unexpected exceptions"""
        db.session.rollback()
        print(f"❌ Unhandled exception: {e}")
        if app.config.get('DEBUG'):
            raise e  # Re-raise in debug mode
        return {'error': 'An unexpected error occurred'}, 500