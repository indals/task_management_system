"""
Route Registration Module

This module handles registration of all route blueprints with the Flask app.
"""

from flask import Flask

def register_all_routes(app: Flask):
    """
    Register all route blueprints with the Flask app.
    
    Args:
        app (Flask): Flask application instance
    """
    
    # Import all blueprints
    try:
        from app.routes.auth_routes import auth_bp
        from app.routes.task_routes import task_bp
        from app.routes.project_routes import project_bp
        from app.routes.comment_routes import comment_bp
        from app.routes.notification_routes import notification_bp
        from app.routes.analytics_routes import analytics_bp
        from app.routes.sprint_routes import sprint_bp
        from app.routes.enum_routes import enum_bp
        
        # Register core functionality routes
        blueprints = [
            (auth_bp, 'Authentication'),
            (task_bp, 'Tasks'),
            (project_bp, 'Projects'),
            (comment_bp, 'Comments'),
            (notification_bp, 'Notifications'),
            (analytics_bp, 'Analytics'),
            (sprint_bp, 'Sprints'),
            (enum_bp, 'Enums')
        ]
        
        for blueprint, name in blueprints:
            app.register_blueprint(blueprint)
            print(f"✅ {name} routes registered")
        
        print("✅ All route blueprints registered successfully!")
        
    except ImportError as e:
        print(f"❌ Error importing routes: {e}")
        raise
    
    # Print registered routes for debugging (development only)
    if app.config.get('DEBUG'):
        print("\n📋 Registered API Routes:")
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                methods = ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
                routes.append(f"  {methods:15} {rule.rule}")
        
        # Sort routes for better readability
        for route in sorted(routes):
            print(route)
        print()