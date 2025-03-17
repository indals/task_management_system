# run.py
from app import create_app, db
from flask_migrate import Migrate
# from app.urls import register_routes

# Create the app
app = create_app('development')  # or any config you are using

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register routes
# register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
