# run.py
from app import create_app, db
from app.urls import register_routes

# Create the app
app = create_app('development')

# Register routes
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)