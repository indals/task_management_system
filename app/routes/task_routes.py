from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.task_comment import TaskComment
from app.models.user import User
from app.services.task_service import TaskService

task_bp = Blueprint('task', __name__, url_prefix='/api/tasks')


@task_bp.route('', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    user_id = data.get('user_id') # Get authenticated user ID
    assigned_to_id = data.get('assigneeId', '')
    result = TaskService.create_task(data, user_id, assigned_to_id)

    if 'error' in result:
        return jsonify(result), 400

    return jsonify(result), 201


@task_bp.route('', methods=['GET'])
@jwt_required()
def get_tasks():
    """
    Retrieves tasks based on user role and query parameters.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)  # Fetch the user object
    if not user:
        return jsonify({'error': 'User not found'}), 404

    status = request.args.get('status')
    assignee = request.args.get('assignee')
    created_by = request.args.get('created_by')
    priority = request.args.get('priority')

    try:
        if user.role.value == 'MANAGER':
            # Manager can fetch tasks created by them or by others (if created_by is provided)
            if created_by:
                tasks = TaskService.get_tasks_created_by_user(created_by)
            else:
                tasks = TaskService.get_tasks_created_by_user(current_user_id)
        else:
            # Normal user can only fetch tasks assigned to them
            tasks = TaskService.get_tasks_by_user(current_user_id)

        return jsonify(tasks), 200

    except Exception as e:
        return jsonify({'error': f'Error fetching tasks: {str(e)}'}), 500





@task_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_one(task_id):
    result = TaskService.get_task_by_id(task_id)

    if 'error' in result:
        return jsonify(result), 404

    # Fetch all comments for the given task
    comments = TaskComment.query.filter_by(task_id=task_id).all()

    # Get unique user IDs from the comments
    user_ids = {comment.user_id for comment in comments}

    # Fetch user details in a single query
    users = User.query.filter(User.id.in_(user_ids)).all()
    user_map = {user.id: {"id": user.id, "name": user.name, "email": user.email} for user in users}

    # Attach user details to comments
    result['comments'] = [
        {
            **comment.to_dict(),
            "author": user_map.get(comment.user_id, {})  # Default to empty if user not found
        } for comment in comments
    ]

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

    # Fetch task and related comments
    task = TaskService.get_task_by_id(task_id)
    if 'error' in task:
        return jsonify(task), 404

    comments = TaskComment.query.filter_by(task_id=task_id).all()
    task['comments'] = [comment.to_dict() for comment in comments]  # Convert comments to JSON

    return jsonify(task), 200

@task_bp.route('/<int:task_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(task_id):
    data = request.get_json()
    print("Received Data:", data)  # Debugging

    if not data:
        return jsonify({'error': 'No JSON payload received'}), 400

    comment_text = data.get("text", "").strip()  # Ensure correct key exists
    print("Extracted Comment Text:", comment_text)  # Debugging

    if not comment_text:
        return jsonify({'error': 'Comment text is required'}), 400

    result = TaskService.add_comment(task_id, get_jwt_identity(), comment_text)

    if 'error' in result:
        return jsonify(result), 400

    return jsonify(result), 201



