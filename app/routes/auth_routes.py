from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')



@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "role")  # Default role is "user"

    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    result = AuthService.register_user(username, email, password, role)

    if 'error' in result:
        return jsonify(result), 400

    return jsonify(result), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    # Call the login_user method from AuthService
    result = AuthService.login_user(email, password)

    if not result:
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify(result), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user = AuthService.validate_token()
    return jsonify(user), 200


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
        return jsonify({'error': 'No fields to update'}), 400

    result = AuthService.update_profile(user_id, data)

    if result:
        return jsonify(result), 200
    return jsonify({'error': 'Failed to update profile'}), 400


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def update_password():
    data = request.get_json()
    user_id = get_jwt_identity()

    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not current_password or not new_password:
        return jsonify({'error': 'Missing required fields'}), 400

    result = AuthService.change_password(user_id, new_password)

    if 'error' in result:
        return jsonify(result), 400

    return jsonify(result), 200

@auth_bp.route('/ping', methods=['GET'])
def test():
    return jsonify({"message": "Auth API is working!"}), 200


@auth_bp.route('/users', methods=['GET'])
@jwt_required()  # Protect this route, only authenticated users can access
def get_users():
    """
    Returns a list of all users with only their id and name.
    """
    users = AuthService.get_all_users_ids_and_names()
    return jsonify(users), 200