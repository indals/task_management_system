"""
WSGI Entry Point for Production Deployment

This file is used by WSGI servers like Gunicorn, uWSGI, or mod_wsgi
to serve the Flask application in production.

Usage:
    gunicorn --bind 0.0.0.0:8000 wsgi:app
    uwsgi --http :8000 --module wsgi:app
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import application factory and route registration
from app import create_app
from app.routes import register_all_routes

# Determine environment
environment = os.getenv('FLASK_ENV', 'production')

# Create application instance
app = create_app(environment)

# Register all routes
register_all_routes(app)

# Application context setup for production
with app.app_context():
    try:
        from app import db
        # Verify database connection
        db.session.execute(db.text('SELECT 1'))
        print(f"✅ WSGI: Application initialized successfully in {environment} mode")
    except Exception as e:
        print(f"❌ WSGI: Database connection failed: {e}")
        # Don't raise the exception as it might prevent the app from starting
        # The health check endpoints will catch database issues

# Export app for WSGI server
if __name__ == "__main__":
    # This allows testing the WSGI app directly
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)))