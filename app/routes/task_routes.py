#task_routes.py
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
    """Get tasks with advanced filtering and pagination."""
    try:
        user_id = get_jwt_identity()
        
        # Extract pagination parameters (accept but ignore for now)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Build filters from query parameters
        filters = {}
        
        # Project and sprint filters
        if request.args.get('project_id'):
            filters['project_id'] = int(request.args.get('project_id'))
        if request.args.get('sprint_id'):
            filters['sprint_id'] = int(request.args.get('sprint_id'))
            
        # User filters
        if request.args.get('assigned_to_id'):
            filters['assigned_to_id'] = int(request.args.get('assigned_to_id'))
        if request.args.get('created_by_id'):
            filters['created_by_id'] = int(request.args.get('created_by_id'))
            
        # Status and priority filters
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        if request.args.get('priority'):
            filters['priority'] = request.args.get('priority')
        if request.args.get('task_type'):
            filters['task_type'] = request.args.get('task_type')
            
        # Special filters
        if request.args.get('overdue') == 'true':
            filters['overdue'] = True
        if request.args.get('parent_task_id'):
            filters['parent_task_id'] = int(request.args.get('parent_task_id'))
        
        # Call existing service method (without pagination for now)
        result, status_code = TaskService.get_tasks_by_filters(user_id, filters)
        
        if status_code != 200:
            return jsonify(result), status_code
        
        # For now, return the original format but with pagination info
        # Later we'll modify this to use actual pagination
        tasks = result
        
        # Simulate pagination response format
        total = len(tasks)
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_tasks = tasks[start_index:end_index]
        
        return jsonify({
            'tasks': paginated_tasks,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
            'has_next': end_index < total,
            'has_prev': page > 1
        }), 200
        
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



@task_bp.route('/overdue', methods=['GET'])
@jwt_required()
def get_overdue_tasks():
    """Get overdue tasks for the current user."""
    try:
        user_id = get_jwt_identity()
        result, status_code = TaskService.get_overdue_tasks(user_id)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error fetching overdue tasks: {str(e)}'}), 500
    

@task_bp.route('/time-logs', methods=['GET'])
@jwt_required()
def get_user_time_logs():
    """Get time logs for the current user."""
    try:
        user_id = get_jwt_identity()
        
        # Get date range parameters
        start_date = request.args.get('start_date')  # YYYY-MM-DD
        end_date = request.args.get('end_date')      # YYYY-MM-DD
        limit = request.args.get('limit', 50, type=int)
        
        result, status_code = TaskService.get_user_time_logs(user_id, start_date, end_date, limit)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error fetching time logs: {str(e)}'}), 500