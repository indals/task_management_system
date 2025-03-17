#wsgi.py
import os
from app import create_app  # Import create_app function from your app/__init__.py
from config import Config

config_name = os.environ.get('FLASK_CONFIG') or 'default'
app = create_app(config_name) # Create the Flask app instance using the factory pattern

# Important: The 'app' variable is what Gunicorn needs.