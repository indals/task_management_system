# app/routes/project_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.project_service import ProjectService
from app.utils.response import (
    success_response, error_response, created_response, 
    not_found_response, validation_error_response, server_error_response
)

project_bp = Blueprint('project', __name__, url_prefix='/api/projects')


@project_bp.route('', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    user_id = get_jwt_identity()

    if not data.get('name'):
        return validation_error_response('Project name is required')

    result = ProjectService.create_project(data, user_id)
    return created_response("Project created successfully", result)


@project_bp.route('', methods=['GET'])
@jwt_required()
def get_all():
    result = ProjectService.get_all_projects()
    return success_response("Projects retrieved successfully", result)


@project_bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def get_one(project_id):
    result = ProjectService.get_project_by_id(project_id)
    return success_response("Project retrieved successfully", result)


@project_bp.route('/<int:project_id>', methods=['PATCH'])
@jwt_required()
def update(project_id):
    data = request.get_json()
    result = ProjectService.update_project(project_id, data)
    return success_response("Project updated successfully", result)


@project_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete(project_id):
    result = ProjectService.delete_project(project_id)
    return success_response("Project deleted successfully", result)


@project_bp.route('/recent', methods=['GET'])
@jwt_required()
def get_recent():
    result = ProjectService.get_recent_projects()
    return success_response("Recent projects retrieved successfully", result)