from app.models.task_comment import TaskComment
from app.models.task import Task
from app.models.user import User
from app import db


class CommentService:
    @staticmethod
    def get_comments_by_task(task_id):
        """Gets all comments for a specific task."""
        comments = TaskComment.query.filter_by(task_id=task_id).all()
        return [comment.to_dict() for comment in comments]

    @staticmethod
    def add_comment(task_id, user_id, comment_text):
        """Adds a new comment to a task."""
        # Verify task exists
        task = Task.query.get_or_404(task_id)

        # Create comment
        comment = TaskComment(
            task_id=task_id,
            user_id=user_id,
            comment=comment_text
        )

        db.session.add(comment)
        db.session.commit()
        return comment.to_dict()

    @staticmethod
    def update_comment(comment_id, user_id, comment_text):
        """Updates an existing comment."""
        comment = TaskComment.query.get_or_404(comment_id)

        # Check if user is the author of the comment
        if comment.user_id != user_id:
            return {'error': 'You are not authorized to edit this comment'}

        comment.comment = comment_text
        db.session.commit()
        return comment.to_dict()

    @staticmethod
    def delete_comment(comment_id, user_id):
        """Deletes a comment."""
        comment = TaskComment.query.get_or_404(comment_id)

        # Check if user is the author of the comment
        if comment.user_id != user_id:
            return {'error': 'You are not authorized to delete this comment'}

        db.session.delete(comment)
        db.session.commit()
        return {'message': 'Comment deleted successfully'}