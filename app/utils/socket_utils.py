# app/utils/socket_utils.py
"""
Socket.IO utilities for real-time communication
"""
from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from flask_jwt_extended import decode_token
from functools import wraps
import json
# from app.models.notification import Notification
# from app.models.user import User

# Initialize SocketIO (will be configured in __init__.py)
socketio = None
connected_users = {}  # sid -> user_id
def init_socketio(app):
    """Initialize SocketIO with the Flask app"""
    global socketio
    socketio = SocketIO(
        app,
        cors_allowed_origins="*",
        async_mode='threading',
        logger=True,
        engineio_logger=True
    )
    register_socket_events()
    return socketio

connected_users = {}  # global mapping: sid -> user_id

def authenticated_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = connected_users.get(request.sid)
        if not user_id:
            emit('error', {'message': 'Authentication required'})
            disconnect()
            return
        kwargs['user_id'] = user_id
        return f(*args, **kwargs)
    return decorated


def register_socket_events():
    """Register all socket event handlers"""
    
    # connected_users = {}  # global mapping: sid -> user_id

    @socketio.on('connect')
    def handle_connect(auth=None):
        """Handle client connection"""
        from flask import request
        print(f"🔌 Client connected: {request.sid}")

        try:
            # Get token from auth data or query parameters
            token = None
            if auth and isinstance(auth, dict):
                token = auth.get('token')
            if not token:
                token = request.args.get('token')

            if not token:
                emit('error', {'message': 'Authentication required'})
                disconnect()
                return

            # Decode token once
            decoded_token = decode_token(token)
            user_id = decoded_token['sub']

            # Store in global mapping
            connected_users[request.sid] = user_id

            # Join user-specific room
            join_room(f"user_{user_id}")

            # Get user info (import locally to avoid circular import)
            from app.models.user import User
            user = User.query.get(user_id)
            if user:
                emit('connected', {
                    'message': f'Welcome {user.email}!',
                    'user_id': user_id,
                    'room': f"user_{user_id}"
                })
                print(f"✅ User {user.email} (ID: {user_id}) connected")
            else:
                emit('error', {'message': 'User not found'})
                disconnect()

        except Exception as e:
            print(f"❌ Authentication error: {e}")
            emit('error', {'message': 'Authentication failed'})
            disconnect()


    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        from flask import request
        print(f"🔌 Client disconnected: {request.sid}") 

    @socketio.on('join_user_room')
    @authenticated_only
    def handle_join_user_room(data, user_id):
        """Join user-specific room for personal notifications"""
        room = f"user_{user_id}"
        join_room(room)
        emit('room_joined', {'room': room, 'message': 'Joined personal notification room'})
        print(f"👤 User {user_id} joined room: {room}")

    @socketio.on('join_project_room')
    @authenticated_only
    def handle_join_project_room(data, user_id):
        """Join project-specific room for project updates"""
        try:
            project_id = data.get('project_id')
            if not project_id:
                emit('error', {'message': 'Project ID required'})
                return
            
            # TODO: Verify user has access to this project
            room = f"project_{project_id}"
            join_room(room)
            emit('room_joined', {'room': room, 'message': f'Joined project {project_id} room'})
            print(f"📁 User {user_id} joined project room: {room}")
            
        except Exception as e:
            emit('error', {'message': f'Failed to join project room: {str(e)}'})

    @socketio.on('get_notifications')
    @authenticated_only
    def handle_get_notifications(data, user_id):
        """Get user notifications via socket"""
        try:
            from app.models.notification import Notification
            
            unread_only = data.get('unread_only', False)
            
            query = Notification.query.filter_by(user_id=user_id)
            if unread_only:
                query = query.filter_by(read=False)
            
            notifications = query.order_by(Notification.created_at.desc()).limit(50).all()
            
            emit('notifications_data', {
                'notifications': [n.to_dict() for n in notifications],
                'total': len(notifications),
                'unread_count': Notification.get_unread_count(user_id)
            })
            
        except Exception as e:
            emit('error', {'message': f'Failed to get notifications: {str(e)}'})


    @socketio.on('mark_notification_read')
    @authenticated_only
    def handle_mark_notification_read(data, user_id):
        """Mark a notification as read via socket"""
        try:
            from app.models.notification import Notification
            
            notification_id = data.get('notification_id')
            if not notification_id:
                emit('error', {'message': 'Notification ID required'})
                return
            
            notification = Notification.query.filter_by(
                id=notification_id, 
                user_id=user_id
            ).first()
            
            if not notification:
                emit('error', {'message': 'Notification not found'})
                return
            
            notification.mark_as_read()
            
            emit('notification_updated', {
                'notification_id': notification_id,
                'status': 'read',
                'unread_count': Notification.get_unread_count(user_id)
            })
            
        except Exception as e:
            emit('error', {'message': f'Failed to mark notification as read: {str(e)}'})

    @socketio.on('ping')
    def handle_ping(data):
        """Handle ping for connection testing"""
        emit('pong', {'message': 'Server is alive', 'timestamp': str(datetime.utcnow())})

# Utility functions for broadcasting notifications
def broadcast_notification(user_id, notification_data):
    """Broadcast a notification to a specific user"""
    if socketio:
        socketio.emit(
            'new_notification', 
            notification_data, 
            room=f"user_{user_id}"
        )
        print(f"📢 Notification sent to user {user_id}: {notification_data.get('title', 'No title')}")

def broadcast_to_project(project_id, event_name, data):
    """Broadcast an event to all users in a project room"""
    if socketio:
        socketio.emit(
            event_name,
            data,
            room=f"project_{project_id}"
        )
        print(f"📢 Broadcast to project {project_id}: {event_name}")

def broadcast_task_update(task_data, project_id=None, assignee_id=None):
    """Broadcast task updates to relevant users"""
    if socketio:
        # Broadcast to project room if project_id exists
        if project_id:
            socketio.emit(
                'task_updated',
                task_data,
                room=f"project_{project_id}"
            )
        
        # Broadcast to assignee's personal room
        if assignee_id:
            socketio.emit(
                'task_updated',
                task_data,
                room=f"user_{assignee_id}"
            )
        
        print(f"📢 Task update broadcast: {task_data.get('id', 'Unknown ID')}")

# Test utility functions
def emit_test_notification(user_id, message="Test notification"):
    """Send a test notification to a specific user (for testing)"""
    test_data = {
        'id': 'test',
        'type': 'info',
        'title': 'Test Notification',
        'message': message,
        'created_at': str(datetime.utcnow())
    }
    broadcast_notification(user_id, test_data)

# Import datetime for timestamps
from datetime import datetime