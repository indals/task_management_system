# run.py
import os
from app import create_app, db
from app.urls import register_routes

# Set environment variables for Flask CLI
os.environ['FLASK_APP'] = 'run.py'
os.environ['FLASK_ENV'] = 'development'

# Create the app with default config
app = create_app('development')

# Register routes
register_routes(app)

# This is needed for Flask CLI commands like 'flask db init'
# Flask CLI will use this app instance
if __name__ == '__main__':
    app.run(debug=True)