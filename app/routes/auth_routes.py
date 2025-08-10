# app/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService
from app.utils.response import (
    success_response, error_response, created_response, 
    not_found_response, validation_error_response, server_error_response,
    unauthorized_response
)

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "EMPLOYEE")  # Default role is "user"

    if not username or not email or not password:
        return validation_error_response('Missing required fields')

    result = AuthService.register_user(username, email, password, role)

    if 'error' in result:
        return error_response(result['error'])

    return created_response("User registered successfully", result)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return validation_error_response('Missing email or password')

    # Call the login_user method from AuthService
    result = AuthService.login_user(email, password)

    if not result["success"]:
        return unauthorized_response(result["error"])

    return success_response("Login successful", result)


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user = AuthService.validate_token()
    return success_response("User profile retrieved successfully", user)


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    data = request.get_json()
    user_id = get_jwt_identity()  # Get the user ID from JWT token

    # Ensure the required fields are present
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # If any required fields are missing, return an error
    if not name and not email and not password:
        return validation_error_response('No fields to update')

    result = AuthService.update_profile(user_id, data)

    if result:
        return success_response("Profile updated successfully", result)
    return error_response('Failed to update profile')


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def update_password():
    data = request.get_json()
    user_id = get_jwt_identity()

    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not current_password or not new_password:
        return validation_error_response('Missing required fields')

    result = AuthService.change_password(user_id, new_password)

    if 'error' in result:
        return error_response(result['error'])

    return success_response("Password changed successfully", result)


@auth_bp.route('/ping', methods=['GET'])
def test():
    return success_response("Auth API is working!")


@auth_bp.route('/users', methods=['GET'])
@jwt_required()  # Protect this route, only authenticated users can access
def get_users():
    """
    Returns a list of all users with only their id and name.
    """
    users = AuthService.get_all_users_ids_and_names()
    return success_response("Users retrieved successfully", users)