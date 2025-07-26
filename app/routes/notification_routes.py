#notification_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.notification_service import NotificationService

notification_bp = Blueprint('notification', __name__, url_prefix='/api/notifications')


# Add this method to app/routes/notification_routes.py

@notification_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_notification_summary():
    """Get notification summary for dashboard."""
    try:
        user_id = get_jwt_identity()
        result = NotificationService.get_notification_summary(user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Error fetching notification summary: {str(e)}'}), 500
    
@notification_bp.route('', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()  # Get authenticated user ID
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'

    result = NotificationService.get_user_notifications(user_id, unread_only)
    return jsonify(result), 200


@notification_bp.route('/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_as_read(notification_id):
    user_id = get_jwt_identity()  # Get authenticated user ID
    result = NotificationService.mark_as_read(notification_id, user_id)

    if 'error' in result:
        return jsonify(result), 404

    return jsonify(result), 200


@notification_bp.route('/read-all', methods=['POST'])
@jwt_required()
def mark_all_as_read():
    user_id = get_jwt_identity()  # Get authenticated user ID
    result = NotificationService.mark_all_notifications_as_read(user_id)
    return jsonify(result), 200


@notification_bp.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete(notification_id):
    user_id = get_jwt_identity()  # Get authenticated user ID
    result = NotificationService.delete_notification(notification_id, user_id)

    if 'error' in result:
        return jsonify(result), 404

    return jsonify({'message': 'Notification deleted successfully'}), 200
