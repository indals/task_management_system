# app/routes/task_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from app.models.task_comment import TaskComment
from app.models.user import User
from app.models.time_log import TimeLog
from app.services.task_service import TaskService
from app.utils.response import (
    success_response, error_response, created_response, 
    not_found_response, validation_error_response, server_error_response
)

task_bp = Blueprint('task', __name__, url_prefix='/api/tasks')


@task_bp.route('', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    user_id = data.get('user_id') # Get authenticated user ID
    assigned_to_id = data.get('assigneeId', '')
    result = TaskService.create_task(data, user_id, assigned_to_id)

    if 'error' in result:
        return error_response(result['error'])

    return created_response("Task created successfully", result)


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
            return error_response(result.get('error', 'Error fetching tasks'), status_code=status_code)
        
        # For now, return the original format but with pagination info
        # Later we'll modify this to use actual pagination
        tasks = result
        
        # Simulate pagination response format
        total = len(tasks)
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_tasks = tasks[start_index:end_index]
        
        response_data = {
            'tasks': paginated_tasks,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
            'has_next': end_index < total,
            'has_prev': page > 1
        }
        
        return success_response("Tasks retrieved successfully", response_data)
        
    except Exception as e:
        return server_error_response(f'Error fetching tasks: {str(e)}')


@task_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_one(task_id):
    result = TaskService.get_task_by_id(task_id)

    if 'error' in result:
        return not_found_response(result['error'])

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

    return success_response("Task retrieved successfully", result)


@task_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update(task_id):
    data = request.get_json()
    result = TaskService.update_task(task_id, data)

    if 'error' in result:
        return not_found_response(result['error'])

    return success_response("Task updated successfully", result)


@task_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete(task_id):
    TaskService.delete_task(task_id)
    return success_response("Task deleted successfully")


@task_bp.route('/<int:task_id>/assign', methods=['POST'])
@jwt_required()
def assign(task_id):
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return validation_error_response('Missing user_id')

    result = TaskService.assign_task(task_id, user_id)

    if 'error' in result:
        return not_found_response(result['error'])

    # Fetch task and related comments
    task = TaskService.get_task_by_id(task_id)
    if 'error' in task:
        return not_found_response(task['error'])

    comments = TaskComment.query.filter_by(task_id=task_id).all()
    task['comments'] = [comment.to_dict() for comment in comments]  # Convert comments to JSON

    return success_response("Task assigned successfully", task)


@task_bp.route('/<int:task_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(task_id):
    data = request.get_json()

    if not data:
        return validation_error_response('No JSON payload received')

    comment_text = data.get("text", "").strip()  # Ensure correct key exists

    if not comment_text:
        return validation_error_response('Comment text is required')

    result = TaskService.add_comment(task_id, get_jwt_identity(), comment_text)

    if 'error' in result:
        return error_response(result['error'])

    return created_response("Comment added successfully", result)


@task_bp.route('/overdue', methods=['GET'])
@jwt_required()
def get_overdue_tasks():
    """Get overdue tasks for the current user."""
    try:
        user_id = get_jwt_identity()
        result, status_code = TaskService.get_overdue_tasks(user_id)
        
        if status_code != 200:
            return error_response(result.get('error', 'Error fetching overdue tasks'), status_code=status_code)
        
        return success_response("Overdue tasks retrieved successfully", result)
        
    except Exception as e:
        return server_error_response(f'Error fetching overdue tasks: {str(e)}')
    

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
        
        if status_code != 200:
            return error_response(result.get('error', 'Error fetching time logs'), status_code=status_code)
        
        return success_response("Time logs retrieved successfully", result)
        
    except Exception as e:
        return server_error_response(f'Error fetching time logs: {str(e)}')
    

@task_bp.route('/<int:task_id>/time', methods=['POST'])
@jwt_required()
def log_time_for_task(task_id):
    """Log time spent on a specific task."""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if not data:
            return validation_error_response('No data provided')
            
        hours = data.get('hours')
        description = data.get('description', '')
        work_date = data.get('work_date')  # Optional, defaults to today
        
        if not hours or hours <= 0:
            return validation_error_response('Valid hours (> 0) are required')
            
        result, status_code = TaskService.log_time(task_id, user_id, hours, description, work_date)
        
        if status_code != 201:
            return error_response(result.get('error', 'Error logging time'), status_code=status_code)
        
        return created_response("Time logged successfully", result)
        
    except Exception as e:
        return server_error_response(f'Error logging time: {str(e)}')


@task_bp.route('/<int:task_id>/time', methods=['GET'])
@jwt_required()
def get_task_time_logs(task_id):
    """Get time logs for a specific task."""
    try:
        user_id = get_jwt_identity()
        result, status_code = TaskService.get_task_time_logs(task_id, user_id)
        
        if status_code != 200:
            return error_response(result.get('error', 'Error fetching time logs'), status_code=status_code)
        
        return success_response("Task time logs retrieved successfully", result)
        
    except Exception as e:
        return server_error_response(f'Error fetching time logs: {str(e)}')


@task_bp.route('/time/daily-summary', methods=['GET'])
@jwt_required()
def get_daily_time_summary():
    """Get daily time summary for the current user."""
    try:
        user_id = get_jwt_identity()
        date = request.args.get('date')  # YYYY-MM-DD format
        
        if not date:
            date = datetime.utcnow().date().isoformat()
            
        daily_hours = TimeLog.get_user_daily_hours(user_id, date)
        
        response_data = {
            'date': date,
            'total_hours': daily_hours,
            'user_id': user_id
        }
        
        return success_response("Daily summary retrieved successfully", response_data)
        
    except Exception as e:
        return server_error_response(f'Error fetching daily summary: {str(e)}')
    

@task_bp.route('/test-response', methods=['GET'])
def test_response():
    try:
        from app.utils.response import success_response
        return success_response("Test successful", {"test": "data"})
    except Exception as e:
        return jsonify({"error": f"Response utility error: {str(e)}"}), 500

# Or add this at the top of your route file to check imports
try:
    from app.utils.response import (
        success_response, error_response, created_response, 
        not_found_response, validation_error_response, server_error_response
    )
    print("✅ Response utilities imported successfully")
except ImportError as e:
    print(f"❌ Response utility import error: {e}")