# app/__init__.py
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Initialize db globally
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name):
    """Factory function to create and configure the Flask app."""
    from flask import Flask
    from config import Config

    # Initialize the Flask app
    app = Flask(__name__)
    app.config.from_object(Config.get_config(config_name))  # Load the appropriate config

    # Enable CORS globally
    CORS(app)  # This allows all origins by default
    # Initialize the db with the app
    db.init_app(app)
    jwt.init_app(app)
    # Register routes, blueprints, etc.
    # from app.urls import register_routes
    # register_routes(app)

    return app
