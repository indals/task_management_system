# app/routes/analytics_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.analytics_service import AnalyticsService
from app.utils.response import (
    success_response, error_response, created_response, 
    not_found_response, validation_error_response, server_error_response
)

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


@analytics_bp.route('/task-completion', methods=['GET'])
@jwt_required()
def task_completion():
    user_id = request.args.get('user_id', None)  # Admins can provide a user_id
    if not user_id:
        user_id = get_jwt_identity()  # Default to authenticated user

    time_period = request.args.get('period', 'month')  # 'week', 'month', 'year'
    
    try:
        result = AnalyticsService.get_task_completion_rate(user_id, time_period)
        
        if isinstance(result, tuple) and len(result) == 2:
            data, status_code = result
            if status_code != 200:
                return error_response(data.get('error', 'Error fetching task completion data'), status_code=status_code)
            result = data
        
        return success_response("Task completion rate retrieved successfully", result)
        
    except Exception as e:
        return server_error_response(f'Error fetching task completion data: {str(e)}')


@analytics_bp.route('/user-productivity', methods=['GET'])
@jwt_required()
def user_productivity():
    user_id = request.args.get('user_id', None)
    if not user_id:
        user_id = get_jwt_identity()

    try:
        result = AnalyticsService.get_user_performance(user_id)
        
        if isinstance(result, tuple) and len(result) == 2:
            data, status_code = result
            if status_code != 200:
                return error_response(data.get('error', 'Error fetching user productivity data'), status_code=status_code)
            result = data
        
        return success_response("User productivity data retrieved successfully", result)
        
    except Exception as e:
        return server_error_response(f'Error fetching user productivity data: {str(e)}')


@analytics_bp.route('/task-status-distribution', methods=['GET'])
@jwt_required()
def task_status_distribution():
    try:
        result = AnalyticsService.get_task_distribution_by_status()
        
        if isinstance(result, tuple) and len(result) == 2:
            data, status_code = result
            if status_code != 200:
                return error_response(data.get('error', 'Error fetching task status distribution'), status_code=status_code)
            result = data
        
        return success_response("Task status distribution retrieved successfully", result)
        
    except Exception as e:
        return server_error_response(f'Error fetching task status distribution: {str(e)}')


@analytics_bp.route('/task-priority-distribution', methods=['GET'])
@jwt_required()
def task_priority_distribution():
    try:
        result = AnalyticsService.get_task_distribution_by_priority()
        
        if isinstance(result, tuple) and len(result) == 2:
            data, status_code = result
            if status_code != 200:
                return error_response(data.get('error', 'Error fetching task priority distribution'), status_code=status_code)
            result = data
        
        return success_response("Task priority distribution retrieved successfully", result)
        
    except Exception as e:
        return server_error_response(f'Error fetching task priority distribution: {str(e)}')