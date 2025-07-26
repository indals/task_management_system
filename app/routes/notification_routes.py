# app/routes/notification_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.notification_service import NotificationService
from app.utils.response import (
    success_response, error_response, created_response, 
    not_found_response, validation_error_response, server_error_response
)

notification_bp = Blueprint('notification', __name__, url_prefix='/api/notifications')


@notification_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_notification_summary():
    """Get notification summary for dashboard."""
    try:
        user_id = get_jwt_identity()
        result = NotificationService.get_notification_summary(user_id)
        
        if 'error' in result:
            return error_response(result['error'])
        
        return success_response("Notification summary retrieved successfully", result)
        
    except Exception as e:
        return server_error_response(f'Error fetching notification summary: {str(e)}')
    

@notification_bp.route('', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()  # Get authenticated user ID
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'

    result = NotificationService.get_user_notifications(user_id, unread_only)
    
    message = "Unread notifications retrieved successfully" if unread_only else "Notifications retrieved successfully"
    return success_response(message, result)


@notification_bp.route('/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_as_read(notification_id):
    user_id = get_jwt_identity()  # Get authenticated user ID
    result = NotificationService.mark_as_read(notification_id, user_id)

    if 'error' in result:
        return not_found_response(result['error'])

    return success_response("Notification marked as read", result)


@notification_bp.route('/read-all', methods=['POST'])
@jwt_required()
def mark_all_as_read():
    user_id = get_jwt_identity()  # Get authenticated user ID
    result = NotificationService.mark_all_notifications_as_read(user_id)
    return success_response("All notifications marked as read", result)


@notification_bp.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete(notification_id):
    user_id = get_jwt_identity()  # Get authenticated user ID
    result = NotificationService.delete_notification(notification_id, user_id)

    if 'error' in result:
        return not_found_response(result['error'])

    return success_response("Notification deleted successfully")