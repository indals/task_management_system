from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.analytics_service import AnalyticsService

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


@analytics_bp.route('/task-completion', methods=['GET'])
@jwt_required()
def task_completion():
    user_id = request.args.get('user_id', None)  # Admins can provide a user_id
    if not user_id:
        user_id = get_jwt_identity()  # Default to authenticated user

    time_period = request.args.get('period', 'month')  # 'week', 'month', 'year'
    result = AnalyticsService.get_task_completion_rate(user_id, time_period)
    return jsonify(result), 200


@analytics_bp.route('/user-productivity', methods=['GET'])
@jwt_required()
def user_productivity():
    user_id = request.args.get('user_id', None)
    if not user_id:
        user_id = get_jwt_identity()

    result = AnalyticsService.get_user_performance(user_id)
    return jsonify(result), 200


@analytics_bp.route('/task-status-distribution', methods=['GET'])
@jwt_required()
def task_status_distribution():
    result = AnalyticsService.get_task_distribution_by_status()
    return jsonify(result), 200


@analytics_bp.route('/task-priority-distribution', methods=['GET'])
@jwt_required()
def task_priority_distribution():
    result = AnalyticsService.get_task_distribution_by_priority()
    return jsonify(result), 200
