from app.models.user import User
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from app import db
from werkzeug.security import generate_password_hash
from app.models.enums import UserRole

class AuthService:
    @staticmethod
    def register_user(username, email, password, role="user"):
        """Registers a new user."""
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"error": "User with this email already exists"}

        hashed_password = generate_password_hash(password)
        try:
            user_role = UserRole[role.upper()]  # Convert role string to UserRole enum
        except KeyError:
            return {"message": "Invalid role"}, 400
        user = User(name=username, email=email, role=user_role, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()

        return {"message": "User registered successfully", "user": user.to_dict()}

    @staticmethod
    def login_user(email, password):
        """Authenticates user and returns JWT tokens."""
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):  # Ensure User model has check_password
            return None  # Invalid credentials

        # Return JWT tokens and user info
        return {
            'access_token': create_access_token(identity=user.id),
            'refresh_token': create_refresh_token(identity=user.id),
            'user': user.to_dict()  # Assuming `to_dict` is implemented in the User model
        }

    @staticmethod
    @jwt_required()
    def validate_token():
        """Validates the JWT access token and returns the user details."""
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        return user.to_dict()

    @staticmethod
    def change_password(user_id, new_password):
        """Changes the user's password."""
        user = User.query.get_or_404(user_id)
        user.set_password(new_password)  # Ensure User model has set_password()
        db.session.commit()
        return user.to_dict()

    @staticmethod
    @jwt_required(refresh=True)
    def refresh_token():
        """Generates a new access token using a valid refresh token."""
        current_user_id = get_jwt_identity()  # Gets user ID from refresh token
        user = User.query.get_or_404(current_user_id)

        return {
            'access_token': create_access_token(identity=user.id),
            'user': user.to_dict()
        }

    @staticmethod
    @jwt_required()
    def update_profile(user_id, data):
        """Updates the user's profile."""
        user = User.query.get_or_404(user_id)  # Fetch the user based on ID

        # If the request includes a password, hash it before updating
        if 'password' in data:
            user.password_hash = generate_password_hash(data['password'])

        if 'email' in data:
            user.email = data['email']

        if 'name' in data:
            user.name = data['name']

        try:
            db.session.commit()
            return {'message': 'Profile updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error updating profile: {str(e)}'}, 400