#!/usr/bin/env python3
"""
Setup script for sample data in the IT Task Management System
This script creates sample users, projects, sprints, and tasks for testing and demonstration.
"""

import os
import sys
from datetime import datetime, timedelta
import json

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.project import Project
from app.models.sprint import Sprint
from app.models.task import Task
from app.models.project_member import ProjectMember
from app.models.enums import (
    UserRole, TaskStatus, TaskPriority, TaskType, 
    ProjectStatus, SprintStatus, EstimationUnit
)

def create_sample_users():
    """Create sample users with different IT roles."""
    users_data = [
        {
            'name': 'Alice Johnson',
            'email': 'alice@company.com',
            'password': 'password123',
            'role': UserRole.PROJECT_MANAGER,
            'skills': ['Project Management', 'Agile', 'Scrum', 'Leadership'],
            'github_username': 'alice-pm',
            'daily_work_hours': 8.0
        },
        {
            'name': 'Bob Smith',
            'email': 'bob@company.com',
            'password': 'password123',
            'role': UserRole.SENIOR_DEVELOPER,
            'skills': ['Python', 'Flask', 'PostgreSQL', 'React', 'Docker'],
            'github_username': 'bob-dev',
            'daily_work_hours': 8.0
        },
        {
            'name': 'Carol Davis',
            'email': 'carol@company.com',
            'password': 'password123',
            'role': UserRole.QA_ENGINEER,
            'skills': ['Testing', 'Selenium', 'Pytest', 'Quality Assurance'],
            'github_username': 'carol-qa',
            'daily_work_hours': 8.0
        },
        {
            'name': 'David Wilson',
            'email': 'david@company.com',
            'password': 'password123',
            'role': UserRole.DEVOPS_ENGINEER,
            'skills': ['Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Terraform'],
            'github_username': 'david-devops',
            'daily_work_hours': 8.0
        },
        {
            'name': 'Eva Martinez',
            'email': 'eva@company.com',
            'password': 'password123',
            'role': UserRole.UI_UX_DESIGNER,
            'skills': ['UI Design', 'UX Research', 'Figma', 'Adobe XD'],
            'github_username': 'eva-design',
            'daily_work_hours': 8.0
        },
        {
            'name': 'Frank Brown',
            'email': 'frank@company.com',
            'password': 'password123',
            'role': UserRole.DEVELOPER,
            'skills': ['JavaScript', 'React', 'Node.js', 'MongoDB'],
            'github_username': 'frank-js',
            'daily_work_hours': 8.0
        }
    ]
    
    users = {}
    for user_data in users_data:
        # Check if user already exists
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            users[user_data['role']] = existing_user
            continue
            
        user = User(
            name=user_data['name'],
            email=user_data['email'],
            role=user_data['role'],
            skills=json.dumps(user_data['skills']),
            github_username=user_data['github_username'],
            daily_work_hours=user_data['daily_work_hours']
        )
        user.set_password(user_data['password'])
        db.session.add(user)
        users[user_data['role']] = user
    
    db.session.commit()
    print("✅ Sample users created successfully!")
    return users

def create_sample_projects(users):
    """Create sample projects."""
    projects_data = [
        {
            'name': 'E-commerce Platform',
            'description': 'Modern e-commerce platform with microservices architecture',
            'status': ProjectStatus.ACTIVE,
            'repository_url': 'https://github.com/company/ecommerce-platform',
            'technology_stack': ['Python', 'Flask', 'PostgreSQL', 'React', 'Docker', 'AWS'],
            'client_name': 'RetailCorp',
            'client_email': 'contact@retailcorp.com',
            'estimated_hours': 2000.0,
            'owner_id': users[UserRole.PROJECT_MANAGER].id
        },
        {
            'name': 'Mobile Banking App',
            'description': 'Secure mobile banking application with biometric authentication',
            'status': ProjectStatus.PLANNING,
            'repository_url': 'https://github.com/company/mobile-banking',
            'technology_stack': ['React Native', 'Node.js', 'MongoDB', 'Firebase'],
            'client_name': 'FinanceBank',
            'client_email': 'tech@financebank.com',
            'estimated_hours': 1500.0,
            'owner_id': users[UserRole.PROJECT_MANAGER].id
        }
    ]
    
    projects = []
    for project_data in projects_data:
        # Check if project already exists
        existing_project = Project.query.filter_by(name=project_data['name']).first()
        if existing_project:
            projects.append(existing_project)
            continue
            
        project = Project(
            name=project_data['name'],
            description=project_data['description'],
            status=project_data['status'],
            repository_url=project_data['repository_url'],
            technology_stack=json.dumps(project_data['technology_stack']),
            client_name=project_data['client_name'],
            client_email=project_data['client_email'],
            estimated_hours=project_data['estimated_hours'],
            owner_id=project_data['owner_id'],
            start_date=datetime.utcnow() - timedelta(days=30),
            end_date=datetime.utcnow() + timedelta(days=120)
        )
        db.session.add(project)
        projects.append(project)
    
    db.session.commit()
    print("✅ Sample projects created successfully!")
    return projects

def create_project_members(projects, users):
    """Add team members to projects."""
    # Add team members to the first project
    project = projects[0]
    team_members = [
        (users[UserRole.SENIOR_DEVELOPER], 'Lead Developer'),
        (users[UserRole.DEVELOPER], 'Frontend Developer'),
        (users[UserRole.QA_ENGINEER], 'QA Lead'),
        (users[UserRole.DEVOPS_ENGINEER], 'DevOps Engineer'),
        (users[UserRole.UI_UX_DESIGNER], 'UI/UX Designer')
    ]
    
    for user, role in team_members:
        existing_member = ProjectMember.query.filter_by(
            project_id=project.id, 
            user_id=user.id
        ).first()
        
        if not existing_member:
            member = ProjectMember(
                project_id=project.id,
                user_id=user.id,
                role=role,
                can_create_tasks=True,
                can_edit_tasks=True,
                can_delete_tasks=role in ['Lead Developer', 'QA Lead'],
                can_manage_sprints=role == 'Lead Developer',
                can_manage_members=False
            )
            db.session.add(member)
    
    db.session.commit()
    print("✅ Project team members added successfully!")

def create_sample_sprints(projects):
    """Create sample sprints."""
    project = projects[0]  # E-commerce platform
    
    sprints_data = [
        {
            'name': 'Sprint 1 - Foundation',
            'description': 'Set up project foundation and basic authentication',
            'status': SprintStatus.COMPLETED,
            'start_date': datetime.utcnow() - timedelta(days=28),
            'end_date': datetime.utcnow() - timedelta(days=14),
            'goal': 'Establish project foundation with user authentication',
            'capacity_hours': 160.0,
            'velocity_points': 32
        },
        {
            'name': 'Sprint 2 - Core Features',
            'description': 'Implement core e-commerce features',
            'status': SprintStatus.ACTIVE,
            'start_date': datetime.utcnow() - timedelta(days=14),
            'end_date': datetime.utcnow(),
            'goal': 'Complete product catalog and shopping cart functionality',
            'capacity_hours': 160.0,
            'velocity_points': 35
        },
        {
            'name': 'Sprint 3 - Payment Integration',
            'description': 'Integrate payment processing and order management',
            'status': SprintStatus.PLANNED,
            'start_date': datetime.utcnow(),
            'end_date': datetime.utcnow() + timedelta(days=14),
            'goal': 'Complete payment processing and order workflow',
            'capacity_hours': 160.0,
            'velocity_points': 30
        }
    ]
    
    sprints = []
    for sprint_data in sprints_data:
        existing_sprint = Sprint.query.filter_by(
            name=sprint_data['name'], 
            project_id=project.id
        ).first()
        
        if existing_sprint:
            sprints.append(existing_sprint)
            continue
            
        sprint = Sprint(
            name=sprint_data['name'],
            description=sprint_data['description'],
            status=sprint_data['status'],
            project_id=project.id,
            start_date=sprint_data['start_date'],
            end_date=sprint_data['end_date'],
            goal=sprint_data['goal'],
            capacity_hours=sprint_data['capacity_hours'],
            velocity_points=sprint_data['velocity_points']
        )
        db.session.add(sprint)
        sprints.append(sprint)
    
    db.session.commit()
    print("✅ Sample sprints created successfully!")
    return sprints

def create_sample_tasks(projects, sprints, users):
    """Create sample tasks."""
    project = projects[0]
    sprint_1, sprint_2, sprint_3 = sprints
    
    tasks_data = [
        # Sprint 1 tasks (completed)
        {
            'title': 'Set up project repository and CI/CD pipeline',
            'description': 'Initialize Git repository, configure GitHub Actions for CI/CD',
            'task_type': TaskType.DEPLOYMENT,
            'status': TaskStatus.DONE,
            'priority': TaskPriority.HIGH,
            'story_points': 5,
            'estimated_hours': 8.0,
            'actual_hours': 6.5,
            'labels': ['devops', 'setup', 'ci-cd'],
            'acceptance_criteria': 'Repository created with working CI/CD pipeline',
            'assigned_to_id': users[UserRole.DEVOPS_ENGINEER].id,
            'created_by_id': users[UserRole.PROJECT_MANAGER].id,
            'project_id': project.id,
            'sprint_id': sprint_1.id,
            'completion_date': datetime.utcnow() - timedelta(days=20)
        },
        {
            'title': 'Implement user authentication system',
            'description': 'Create JWT-based authentication with login/register functionality',
            'task_type': TaskType.FEATURE,
            'status': TaskStatus.DONE,
            'priority': TaskPriority.HIGH,
            'story_points': 8,
            'estimated_hours': 16.0,
            'actual_hours': 18.0,
            'labels': ['backend', 'authentication', 'security'],
            'acceptance_criteria': 'Users can register, login, and access protected routes',
            'assigned_to_id': users[UserRole.SENIOR_DEVELOPER].id,
            'created_by_id': users[UserRole.PROJECT_MANAGER].id,
            'project_id': project.id,
            'sprint_id': sprint_1.id,
            'completion_date': datetime.utcnow() - timedelta(days=18)
        },
        {
            'title': 'Design user interface mockups',
            'description': 'Create high-fidelity mockups for main application screens',
            'task_type': TaskType.FEATURE,
            'status': TaskStatus.DONE,
            'priority': TaskPriority.MEDIUM,
            'story_points': 5,
            'estimated_hours': 12.0,
            'actual_hours': 14.0,
            'labels': ['design', 'ui', 'mockups'],
            'acceptance_criteria': 'Complete mockups for all main screens approved by stakeholders',
            'assigned_to_id': users[UserRole.UI_UX_DESIGNER].id,
            'created_by_id': users[UserRole.PROJECT_MANAGER].id,
            'project_id': project.id,
            'sprint_id': sprint_1.id,
            'completion_date': datetime.utcnow() - timedelta(days=16)
        },
        
        # Sprint 2 tasks (in progress)
        {
            'title': 'Implement product catalog API',
            'description': 'Create REST API endpoints for product management',
            'task_type': TaskType.FEATURE,
            'status': TaskStatus.IN_PROGRESS,
            'priority': TaskPriority.HIGH,
            'story_points': 8,
            'estimated_hours': 20.0,
            'actual_hours': 12.0,
            'labels': ['backend', 'api', 'products'],
            'acceptance_criteria': 'CRUD operations for products with proper validation',
            'assigned_to_id': users[UserRole.SENIOR_DEVELOPER].id,
            'created_by_id': users[UserRole.PROJECT_MANAGER].id,
            'project_id': project.id,
            'sprint_id': sprint_2.id,
            'due_date': datetime.utcnow() + timedelta(days=3)
        },
        {
            'title': 'Build shopping cart functionality',
            'description': 'Implement shopping cart with add/remove/update items',
            'task_type': TaskType.FEATURE,
            'status': TaskStatus.TODO,
            'priority': TaskPriority.HIGH,
            'story_points': 6,
            'estimated_hours': 16.0,
            'actual_hours': 0.0,
            'labels': ['frontend', 'cart', 'react'],
            'acceptance_criteria': 'Users can add/remove items and see cart total',
            'assigned_to_id': users[UserRole.DEVELOPER].id,
            'created_by_id': users[UserRole.PROJECT_MANAGER].id,
            'project_id': project.id,
            'sprint_id': sprint_2.id,
            'due_date': datetime.utcnow() + timedelta(days=5)
        },
        {
            'title': 'Write automated tests for authentication',
            'description': 'Create comprehensive test suite for auth endpoints',
            'task_type': TaskType.TESTING,
            'status': TaskStatus.IN_REVIEW,
            'priority': TaskPriority.MEDIUM,
            'story_points': 4,
            'estimated_hours': 8.0,
            'actual_hours': 7.0,
            'labels': ['testing', 'backend', 'authentication'],
            'acceptance_criteria': 'Test coverage > 90% for authentication module',
            'assigned_to_id': users[UserRole.QA_ENGINEER].id,
            'created_by_id': users[UserRole.PROJECT_MANAGER].id,
            'project_id': project.id,
            'sprint_id': sprint_2.id,
            'due_date': datetime.utcnow() + timedelta(days=2)
        },
        
        # Sprint 3 tasks (planned)
        {
            'title': 'Integrate Stripe payment processing',
            'description': 'Implement secure payment processing with Stripe API',
            'task_type': TaskType.FEATURE,
            'status': TaskStatus.BACKLOG,
            'priority': TaskPriority.CRITICAL,
            'story_points': 10,
            'estimated_hours': 24.0,
            'actual_hours': 0.0,
            'labels': ['backend', 'payments', 'stripe'],
            'acceptance_criteria': 'Users can complete purchases securely',
            'assigned_to_id': users[UserRole.SENIOR_DEVELOPER].id,
            'created_by_id': users[UserRole.PROJECT_MANAGER].id,
            'project_id': project.id,
            'sprint_id': sprint_3.id,
            'due_date': datetime.utcnow() + timedelta(days=20)
        },
        {
            'title': 'Implement order management system',
            'description': 'Create order tracking and management functionality',
            'task_type': TaskType.FEATURE,
            'status': TaskStatus.BACKLOG,
            'priority': TaskPriority.HIGH,
            'story_points': 7,
            'estimated_hours': 18.0,
            'actual_hours': 0.0,
            'labels': ['backend', 'orders', 'management'],
            'acceptance_criteria': 'Admin can view and manage all orders',
            'assigned_to_id': users[UserRole.DEVELOPER].id,
            'created_by_id': users[UserRole.PROJECT_MANAGER].id,
            'project_id': project.id,
            'sprint_id': sprint_3.id,
            'due_date': datetime.utcnow() + timedelta(days=25)
        },
        
        # Backlog tasks (no sprint assigned)
        {
            'title': 'Performance optimization',
            'description': 'Optimize database queries and API response times',
            'task_type': TaskType.ENHANCEMENT,
            'status': TaskStatus.BACKLOG,
            'priority': TaskPriority.LOW,
            'story_points': 5,
            'estimated_hours': 12.0,
            'actual_hours': 0.0,
            'labels': ['performance', 'optimization', 'backend'],
            'acceptance_criteria': 'API response times improved by 30%',
            'assigned_to_id': users[UserRole.SENIOR_DEVELOPER].id,
            'created_by_id': users[UserRole.PROJECT_MANAGER].id,
            'project_id': project.id,
            'due_date': datetime.utcnow() + timedelta(days=45)
        }
    ]
    
    for task_data in tasks_data:
        existing_task = Task.query.filter_by(
            title=task_data['title'], 
            project_id=project.id
        ).first()
        
        if existing_task:
            continue
            
        task = Task(
            title=task_data['title'],
            description=task_data['description'],
            task_type=task_data['task_type'],
            status=task_data['status'],
            priority=task_data['priority'],
            story_points=task_data['story_points'],
            estimated_hours=task_data['estimated_hours'],
            actual_hours=task_data['actual_hours'],
            labels=json.dumps(task_data['labels']),
            acceptance_criteria=task_data['acceptance_criteria'],
            assigned_to_id=task_data['assigned_to_id'],
            created_by_id=task_data['created_by_id'],
            project_id=task_data['project_id'],
            sprint_id=task_data.get('sprint_id'),
            due_date=task_data.get('due_date'),
            completion_date=task_data.get('completion_date')
        )
        db.session.add(task)
    
    db.session.commit()
    print("✅ Sample tasks created successfully!")

def main():
    """Main function to set up sample data."""
    print("🚀 Setting up sample data for IT Task Management System...")
    
    # Create Flask app and database tables
    app = create_app('development')
    
    with app.app_context():
        # Create all database tables
        db.create_all()
        print("✅ Database tables created!")
        
        # Create sample data
        users = create_sample_users()
        projects = create_sample_projects(users)
        create_project_members(projects, users)
        sprints = create_sample_sprints(projects)
        create_sample_tasks(projects, sprints, users)
        
        print("\n🎉 Sample data setup completed successfully!")
        print("\n📋 Sample Data Summary:")
        print(f"   👥 Users: {User.query.count()}")
        print(f"   📁 Projects: {Project.query.count()}")
        print(f"   🏃 Sprints: {Sprint.query.count()}")
        print(f"   📝 Tasks: {Task.query.count()}")
        print(f"   👨‍💼 Project Members: {ProjectMember.query.count()}")
        
        print("\n🔑 Sample Login Credentials:")
        for user in User.query.all():
            print(f"   📧 {user.email} | 🔑 password123 | 👤 {user.role.value}")

if __name__ == '__main__':
    main()