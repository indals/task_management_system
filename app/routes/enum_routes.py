# app/routes/enum_routes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models.enums import get_all_enums
from app.utils.response import (
    success_response, error_response, created_response, 
    not_found_response, validation_error_response, server_error_response
)

enum_bp = Blueprint('enums', __name__, url_prefix='/api/enums')

@enum_bp.route('', methods=['GET'])
@jwt_required()
def get_all_enums_endpoint():
    """Get all enum values for the frontend."""
    try:
        enums = get_all_enums()
        return success_response("All enums retrieved successfully", enums)
    except Exception as e:
        return server_error_response(f'Error fetching enums: {str(e)}')

@enum_bp.route('/user-roles', methods=['GET'])
@jwt_required()
def get_user_roles():
    """Get user role options."""
    try:
        from app.models.enums import UserRole, enum_to_dict
        roles = enum_to_dict(UserRole)
        return success_response("User roles retrieved successfully", roles)
    except Exception as e:
        return server_error_response(f'Error fetching user roles: {str(e)}')

@enum_bp.route('/task-statuses', methods=['GET'])
@jwt_required()
def get_task_statuses():
    """Get task status options."""
    try:
        from app.models.enums import TaskStatus, enum_to_dict
        statuses = enum_to_dict(TaskStatus)
        return success_response("Task statuses retrieved successfully", statuses)
    except Exception as e:
        return server_error_response(f'Error fetching task statuses: {str(e)}')

@enum_bp.route('/task-priorities', methods=['GET'])
@jwt_required()
def get_task_priorities():
    """Get task priority options."""
    try:
        from app.models.enums import TaskPriority, enum_to_dict
        priorities = enum_to_dict(TaskPriority)
        return success_response("Task priorities retrieved successfully", priorities)
    except Exception as e:
        return server_error_response(f'Error fetching task priorities: {str(e)}')

@enum_bp.route('/task-types', methods=['GET'])
@jwt_required()
def get_task_types():
    """Get task type options."""
    try:
        from app.models.enums import TaskType, enum_to_dict
        types = enum_to_dict(TaskType)
        return success_response("Task types retrieved successfully", types)
    except Exception as e:
        return server_error_response(f'Error fetching task types: {str(e)}')

@enum_bp.route('/project-statuses', methods=['GET'])
@jwt_required()
def get_project_statuses():
    """Get project status options."""
    try:
        from app.models.enums import ProjectStatus, enum_to_dict
        statuses = enum_to_dict(ProjectStatus)
        return success_response("Project statuses retrieved successfully", statuses)
    except Exception as e:
        return server_error_response(f'Error fetching project statuses: {str(e)}')

@enum_bp.route('/sprint-statuses', methods=['GET'])
@jwt_required()
def get_sprint_statuses():
    """Get sprint status options."""
    try:
        from app.models.enums import SprintStatus, enum_to_dict
        statuses = enum_to_dict(SprintStatus)
        return success_response("Sprint statuses retrieved successfully", statuses)
    except Exception as e:
        return server_error_response(f'Error fetching sprint statuses: {str(e)}')