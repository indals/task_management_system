#urls.py
from app.routes.auth_routes import auth_bp  # Import auth_bp from auth_routes
from app.routes.task_routes import task_bp
from app.routes.notification_routes import notification_bp
from app.routes.analytics_routes import analytics_bp


def register_routes(app):
    """
    Register all blueprints/routes with the Flask application
    """
    from app.routes.auth_routes import auth_bp  # Import inside function
    from app.routes.task_routes import task_bp
    from app.routes.notification_routes import notification_bp
    from app.routes.analytics_routes import analytics_bp
    from app.routes.project_routes import project_bp
    from app.routes.comment_routes import comment_bp

    # Register blueprints


    print(f"Registered Blueprints Before: {app.blueprints.keys()}")  # Debugging
    app.register_blueprint(project_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(auth_bp)  # Register auth_bp blueprint
    app.register_blueprint(task_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(analytics_bp)
    print(f"Registered Blueprints after: {app.blueprints.keys()}")  # Debugging