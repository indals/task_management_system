from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task_comment import TaskComment
from app.models.user import User
from app.services.task_service import TaskService

task_bp = Blueprint('task', __name__, url_prefix='/api/tasks')

@task_bp.route('', methods=['POST'])
@jwt_required()
def create():
    """Create a new task with enhanced features."""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        if not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        
        result, status_code = TaskService.create_task(data, user_id)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error creating task: {str(e)}'}), 500

@task_bp.route('', methods=['GET'])
@jwt_required()
def get_tasks():
    """Get tasks with advanced filtering."""
    try:
        user_id = get_jwt_identity()
        
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
        
        result, status_code = TaskService.get_tasks_by_filters(user_id, filters)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error fetching tasks: {str(e)}'}), 500

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

@task_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_one(task_id):
    """Get task by ID with comments."""
    try:
        user_id = get_jwt_identity()
        result, status_code = TaskService.get_task_by_id(task_id, user_id)
        
        if status_code != 200:
            return jsonify(result), status_code

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
                "author": user_map.get(comment.user_id, {})
            } for comment in comments
        ]

        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'Error fetching task: {str(e)}'}), 500

@task_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update(task_id):
    """Update task with enhanced features."""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        result, status_code = TaskService.update_task(task_id, data, user_id)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error updating task: {str(e)}'}), 500

@task_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete(task_id):
    """Delete task."""
    try:
        user_id = get_jwt_identity()
        result, status_code = TaskService.delete_task(task_id, user_id)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error deleting task: {str(e)}'}), 500

@task_bp.route('/<int:task_id>/assign', methods=['POST'])
@jwt_required()
def assign(task_id):
    """Assign task to a user."""
    try:
        data = request.get_json()
        assigner_id = get_jwt_identity()
        
        if not data or not data.get('user_id'):
            return jsonify({'error': 'Missing user_id'}), 400

        result, status_code = TaskService.assign_task(task_id, data['user_id'], assigner_id)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error assigning task: {str(e)}'}), 500

@task_bp.route('/<int:task_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(task_id):
    """Add a comment to a task."""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if not data:
            return jsonify({'error': 'No JSON payload received'}), 400

        comment_text = data.get("text", "").strip()
        
        if not comment_text:
            return jsonify({'error': 'Comment text is required'}), 400

        result, status_code = TaskService.add_comment(task_id, user_id, comment_text)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error adding comment: {str(e)}'}), 500

@task_bp.route('/<int:task_id>/time', methods=['POST'])
@jwt_required()
def log_time(task_id):
    """Log time spent on a task."""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        hours = data.get('hours')
        if not hours or hours <= 0:
            return jsonify({'error': 'Valid hours value is required'}), 400
            
        description = data.get('description', '')
        work_date = data.get('work_date')
        
        result, status_code = TaskService.log_time(task_id, user_id, hours, description, work_date)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error logging time: {str(e)}'}), 500

@task_bp.route('/<int:task_id>/time', methods=['GET'])
@jwt_required()
def get_time_logs(task_id):
    """Get time logs for a task."""
    try:
        user_id = get_jwt_identity()
        result, status_code = TaskService.get_task_time_logs(task_id, user_id)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error fetching time logs: {str(e)}'}), 500




