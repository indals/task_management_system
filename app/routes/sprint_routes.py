# app/routes/sprint_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.sprint_service import SprintService

sprint_bp = Blueprint('sprint', __name__, url_prefix='/api/sprints')

@sprint_bp.route('', methods=['POST'])
@jwt_required()
def create_sprint():
    """Create a new sprint."""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        required_fields = ['name', 'project_id', 'start_date', 'end_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        result, status_code = SprintService.create_sprint(data, user_id)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error creating sprint: {str(e)}'}), 500

@sprint_bp.route('/<int:sprint_id>', methods=['GET'])
@jwt_required()
def get_sprint(sprint_id):
    """Get sprint by ID."""
    try:
        include_tasks = request.args.get('include_tasks', 'false').lower() == 'true'
        result, status_code = SprintService.get_sprint_by_id(sprint_id, include_tasks)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error fetching sprint: {str(e)}'}), 500

@sprint_bp.route('/<int:sprint_id>', methods=['PUT'])
@jwt_required()
def update_sprint(sprint_id):
    """Update sprint."""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        result, status_code = SprintService.update_sprint(sprint_id, data, user_id)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error updating sprint: {str(e)}'}), 500

@sprint_bp.route('/<int:sprint_id>', methods=['DELETE'])
@jwt_required()
def delete_sprint(sprint_id):
    """Delete sprint."""
    try:
        user_id = get_jwt_identity()
        result, status_code = SprintService.delete_sprint(sprint_id, user_id)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error deleting sprint: {str(e)}'}), 500

@sprint_bp.route('/project/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project_sprints(project_id):
    """Get all sprints for a project."""
    try:
        user_id = get_jwt_identity()
        result, status_code = SprintService.get_project_sprints(project_id, user_id)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error fetching project sprints: {str(e)}'}), 500

@sprint_bp.route('/<int:sprint_id>/start', methods=['POST'])
@jwt_required()
def start_sprint(sprint_id):
    """Start a sprint."""
    try:
        user_id = get_jwt_identity()
        result, status_code = SprintService.start_sprint(sprint_id, user_id)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error starting sprint: {str(e)}'}), 500

@sprint_bp.route('/<int:sprint_id>/complete', methods=['POST'])
@jwt_required()
def complete_sprint(sprint_id):
    """Complete a sprint."""
    try:
        user_id = get_jwt_identity()
        result, status_code = SprintService.complete_sprint(sprint_id, user_id)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error completing sprint: {str(e)}'}), 500

@sprint_bp.route('/<int:sprint_id>/burndown', methods=['GET'])
@jwt_required()
def get_sprint_burndown(sprint_id):
    """Get sprint burndown chart data."""
    try:
        user_id = get_jwt_identity()
        result, status_code = SprintService.get_sprint_burndown(sprint_id, user_id)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error fetching burndown data: {str(e)}'}), 500

@sprint_bp.route('/<int:sprint_id>/tasks/<int:task_id>', methods=['POST'])
@jwt_required()
def add_task_to_sprint(sprint_id, task_id):
    """Add a task to a sprint."""
    try:
        user_id = get_jwt_identity()
        result, status_code = SprintService.add_task_to_sprint(sprint_id, task_id, user_id)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error adding task to sprint: {str(e)}'}), 500

@sprint_bp.route('/<int:sprint_id>/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def remove_task_from_sprint(sprint_id, task_id):
    """Remove a task from a sprint."""
    try:
        user_id = get_jwt_identity()
        result, status_code = SprintService.remove_task_from_sprint(sprint_id, task_id, user_id)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({'error': f'Error removing task from sprint: {str(e)}'}), 500