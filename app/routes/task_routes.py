from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.task_service import TaskService

task_bp = Blueprint('task', __name__, url_prefix='/api/tasks')


@task_bp.route('', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    user_id = get_jwt_identity()  # Get authenticated user ID

    result = TaskService.create_task(data, user_id)

    if 'error' in result:
        return jsonify(result), 400

    return jsonify(result), 201


@task_bp.route('', methods=['GET'])
@jwt_required()
def get_all():
    status = request.args.get('status')
    assignee = request.args.get('assignee')
    priority = request.args.get('priority')

    result = TaskService.get_tasks_by_status(status) if status else TaskService.get_tasks_by_user(assignee)
    return jsonify(result), 200


@task_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_one(task_id):
    result = TaskService.get_task_by_id(task_id)

    if 'error' in result:
        return jsonify(result), 404

    return jsonify(result), 200


@task_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update(task_id):
    data = request.get_json()
    result = TaskService.update_task(task_id, data)

    if 'error' in result:
        return jsonify(result), 404

    return jsonify(result), 200


@task_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete(task_id):
    TaskService.delete_task(task_id)
    return jsonify({'message': 'Task deleted successfully'}), 200


@task_bp.route('/<int:task_id>/assign', methods=['POST'])
@jwt_required()
def assign(task_id):
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400

    result = TaskService.assign_task(task_id, user_id)

    if 'error' in result:
        return jsonify(result), 404

    return jsonify(result), 200
