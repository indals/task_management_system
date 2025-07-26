#project_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.project_service import ProjectService

project_bp = Blueprint('project', __name__, url_prefix='/api/projects')


@project_bp.route('', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    user_id = get_jwt_identity()

    if not data.get('name'):
        return jsonify({'error': 'Project name is required'}), 400

    result = ProjectService.create_project(data, user_id)
    return jsonify(result), 201


@project_bp.route('', methods=['GET'])
@jwt_required()
def get_all():
    result = ProjectService.get_all_projects()
    return jsonify(result), 200


@project_bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def get_one(project_id):
    result = ProjectService.get_project_by_id(project_id)
    return jsonify(result), 200


@project_bp.route('/<int:project_id>', methods=['PATCH'])
@jwt_required()
def update(project_id):
    data = request.get_json()
    result = ProjectService.update_project(project_id, data)
    return jsonify(result), 200


@project_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete(project_id):
    result = ProjectService.delete_project(project_id)
    return jsonify(result), 200


@project_bp.route('/recent', methods=['GET'])
@jwt_required()
def get_recent():
    result = ProjectService.get_recent_projects()
    return jsonify(result), 200