from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.comment_service import CommentService

comment_bp = Blueprint('comment', __name__, url_prefix='/api/tasks')


@comment_bp.route('/<int:task_id>/comments', methods=['GET'])
@jwt_required()
def get_comments(task_id):
    result = CommentService.get_comments_by_task(task_id)
    return jsonify(result), 200


# @comment_bp.route('/<int:task_id>/comments', methods=['POST'])
# @jwt_required()
# def add_comment(task_id):
#     data = request.get_json()
#     user_id = get_jwt_identity()
#
#     if not data.get('comment'):
#         return jsonify({'error': 'Comment text is required'}), 400
#
#     result = CommentService.add_comment(task_id, user_id, data.get('comment'))
#     return jsonify(result), 201


@comment_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    data = request.get_json()
    user_id = get_jwt_identity()

    if not data.get('comment'):
        return jsonify({'error': 'Comment text is required'}), 400

    result = CommentService.update_comment(comment_id, user_id, data.get('comment'))

    if 'error' in result:
        return jsonify(result), 403

    return jsonify(result), 200


@comment_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    user_id = get_jwt_identity()
    result = CommentService.delete_comment(comment_id, user_id)

    if 'error' in result:
        return jsonify(result), 403

    return jsonify(result), 200