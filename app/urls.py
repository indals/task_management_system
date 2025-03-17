from flask import Flask
from app.routes.auth_routes import auth_bp  # Import auth_bp from auth_routes
from app.routes.task_routes import task_bp
from app.routes.notification_routes import notification_bp
from app.routes.analytics_routes import analytics_bp

def register_routes(app: Flask):
    """
    Register all blueprints/routes with the Flask application
    """
    app.register_blueprint(auth_bp)  # Register auth_bp blueprint
    app.register_blueprint(task_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(analytics_bp)
