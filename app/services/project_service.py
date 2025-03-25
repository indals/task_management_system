from app.models.project import Project
from app.models.user import User
from app import db


class ProjectService:
    @staticmethod
    def create_project(data, user_id):
        """Creates a new project."""
        owner = User.query.get_or_404(user_id)

        project = Project(
            name=data.get('name'),
            description=data.get('description'),
            owner_id=owner.id,
            status=data.get('status', 'active')
        )

        db.session.add(project)
        db.session.commit()
        return project.to_dict()

    @staticmethod
    def get_all_projects():
        """Gets all projects."""
        projects = Project.query.all()
        return [project.to_dict() for project in projects]

    @staticmethod
    def get_project_by_id(project_id):
        """Gets a specific project by ID."""
        project = Project.query.get_or_404(project_id)
        return project.to_dict()

    @staticmethod
    def update_project(project_id, data):
        """Updates an existing project."""
        project = Project.query.get_or_404(project_id)

        if 'name' in data:
            project.name = data.get('name')

        if 'description' in data:
            project.description = data.get('description')

        if 'status' in data:
            project.status = data.get('status')

        db.session.commit()
        return project.to_dict()

    @staticmethod
    def delete_project(project_id):
        """Deletes a project."""
        project = Project.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return {'message': 'Project deleted successfully'}

    @staticmethod
    def get_recent_projects():
        """Gets the most recently updated projects."""
        projects = Project.query.order_by(Project.updated_at.desc()).limit(5).all()
        return [project.to_dict() for project in projects]