#!/usr/bin/env python3
"""
Task Management System - Main Application Entry Point

This is the main entry point for the Flask application.
Run with: python app.py
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.routes import register_all_routes

def main():
    """Main application function."""
    # Get environment from environment variable, default to development
    env = os.getenv('FLASK_ENV', 'development')
    
    # Create the Flask application
    app = create_app(env)
    
    # Register all routes
    register_all_routes(app)
    
    # Print startup information
    print(f"🚀 Starting Task Management System in {env} mode")
    print(f"📊 Database: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')}")
    print(f"🔒 Debug Mode: {app.config.get('DEBUG', False)}")
    
    # Create database tables if they don't exist (for development)
    if env == 'development':
        with app.app_context():
            try:
                db.create_all()
                print("✅ Database tables created/verified")
            except Exception as e:
                print(f"⚠️  Database initialization warning: {e}")
    
    # Get host and port from environment variables
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 'on']
    
    # Run the application
    # app.run(
    #     host=host,
    #     port=port,
    #     debug=debug,
    #     threaded=True
    # )

    print(f"🌐 Server will start on http://{host}:{port}")
    print(f"🧪 To test sockets, run: python test_socket_client.py")
    print("=" * 60)
    
    # Run the application with Socket.IO support
    # Run the application with Socket.IO support
    if hasattr(app, 'socketio'):
        app.socketio.run(
            app, 
            host=host, 
            port=port, 
            debug=debug,
            allow_unsafe_werkzeug=True  # Allow for development/testing
        )
    else:
        app.run(host=host, port=port, debug=debug, threaded=True)

if __name__ == '__main__':
    main()