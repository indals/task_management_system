# app/routes/enum_routes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models.enums import get_all_enums

enum_bp = Blueprint('enums', __name__, url_prefix='/api/enums')

@enum_bp.route('', methods=['GET'])
@jwt_required()
def get_all_enums_endpoint():
    """Get all enum values for the frontend."""
    try:
        enums = get_all_enums()
        return jsonify(enums), 200
    except Exception as e:
        return jsonify({'error': f'Error fetching enums: {str(e)}'}), 500

@enum_bp.route('/user-roles', methods=['GET'])
@jwt_required()
def get_user_roles():
    """Get user role options."""
    try:
        from app.models.enums import UserRole, enum_to_dict
        return jsonify(enum_to_dict(UserRole)), 200
    except Exception as e:
        return jsonify({'error': f'Error fetching user roles: {str(e)}'}), 500

@enum_bp.route('/task-statuses', methods=['GET'])
@jwt_required()
def get_task_statuses():
    """Get task status options."""
    try:
        from app.models.enums import TaskStatus, enum_to_dict
        return jsonify(enum_to_dict(TaskStatus)), 200
    except Exception as e:
        return jsonify({'error': f'Error fetching task statuses: {str(e)}'}), 500

@enum_bp.route('/task-priorities', methods=['GET'])
@jwt_required()
def get_task_priorities():
    """Get task priority options."""
    try:
        from app.models.enums import TaskPriority, enum_to_dict
        return jsonify(enum_to_dict(TaskPriority)), 200
    except Exception as e:
        return jsonify({'error': f'Error fetching task priorities: {str(e)}'}), 500

@enum_bp.route('/task-types', methods=['GET'])
@jwt_required()
def get_task_types():
    """Get task type options."""
    try:
        from app.models.enums import TaskType, enum_to_dict
        return jsonify(enum_to_dict(TaskType)), 200
    except Exception as e:
        return jsonify({'error': f'Error fetching task types: {str(e)}'}), 500

@enum_bp.route('/project-statuses', methods=['GET'])
@jwt_required()
def get_project_statuses():
    """Get project status options."""
    try:
        from app.models.enums import ProjectStatus, enum_to_dict
        return jsonify(enum_to_dict(ProjectStatus)), 200
    except Exception as e:
        return jsonify({'error': f'Error fetching project statuses: {str(e)}'}), 500

@enum_bp.route('/sprint-statuses', methods=['GET'])
@jwt_required()
def get_sprint_statuses():
    """Get sprint status options."""
    try:
        from app.models.enums import SprintStatus, enum_to_dict
        return jsonify(enum_to_dict(SprintStatus)), 200
    except Exception as e:
        return jsonify({'error': f'Error fetching sprint statuses: {str(e)}'}), 500