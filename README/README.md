<<<<<<< Updated upstream
# IT Task Management System - Backend API
=======
# Migrations folder remove करें
rm -rf migrations/

# Fresh try करें
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

>>>>>>> Stashed changes

A comprehensive Flask-based REST API for managing tasks, projects, and sprints in IT environments. This system provides advanced features for agile project management, time tracking, team collaboration, and analytics.

## 🚀 Features

### Core Functionality
- **User Management**: Role-based access control with IT-specific roles
- **Task Management**: Advanced task creation with story points, estimation, and dependencies
- **Project Management**: Full project lifecycle management with team collaboration
- **Sprint Management**: Agile sprint planning and execution with burndown charts
- **Time Tracking**: Detailed time logging and reporting
- **Notifications**: Real-time notifications for task updates and assignments
- **Analytics**: Comprehensive dashboards and reporting

### IT-Specific Features
- **Task Types**: Feature, Bug, Enhancement, Refactor, Documentation, Testing, Deployment, Research, Maintenance, Security
- **User Roles**: Admin, Project Manager, Team Lead, Senior Developer, Developer, QA Engineer, DevOps Engineer, UI/UX Designer, Business Analyst, Product Owner, Scrum Master
- **Advanced Status Tracking**: Backlog, Todo, In Progress, In Review, Testing, Blocked, Done, Cancelled, Deployed
- **Story Points & Estimation**: Support for agile estimation techniques
- **Task Dependencies**: Parent-child task relationships
- **Labels & Tags**: Flexible task categorization
- **File Attachments**: Support for code files, documents, and images

## 🏗️ Architecture

```
task_management_system/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/                  # Database models
│   │   ├── user.py             # User model with IT roles
│   │   ├── task.py             # Enhanced task model
│   │   ├── project.py          # Project management
│   │   ├── sprint.py           # Sprint/iteration management
│   │   ├── time_log.py         # Time tracking
│   │   ├── task_attachment.py  # File attachments
│   │   ├── project_member.py   # Team membership
│   │   ├── notification.py     # Notification system
│   │   └── enums.py           # System enumerations
│   ├── services/               # Business logic layer
│   │   ├── auth_service.py     # Authentication & authorization
│   │   ├── task_service.py     # Task management logic
│   │   ├── sprint_service.py   # Sprint management
│   │   ├── project_service.py  # Project operations
│   │   └── analytics_service.py # Reporting & analytics
│   ├── routes/                 # API endpoints
│   │   ├── auth_routes.py      # Authentication endpoints
│   │   ├── task_routes.py      # Task CRUD operations
│   │   ├── sprint_routes.py    # Sprint management
│   │   ├── project_routes.py   # Project operations
│   │   ├── enum_routes.py      # Enum values for frontend
│   │   └── analytics_routes.py # Analytics endpoints
│   └── utils/                  # Utility functions
├── migrations/                 # Database migrations
├── config.py                   # Configuration management
├── run.py                     # Application entry point
└── requirements.txt           # Python dependencies
```

## 🛠️ Technology Stack

- **Framework**: Flask 2.x
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Migrations**: Flask-Migrate with Alembic
- **CORS**: Flask-CORS for cross-origin requests
- **Testing**: Pytest with Flask testing utilities
- **Background Tasks**: Celery with Redis
- **File Processing**: Pillow for image handling
- **Rate Limiting**: Flask-Limiter

## 📋 Database Schema

### Core Models

#### User Model
```python
- id: Primary key
- name: Full name
- email: Unique email address
- role: IT-specific role (Developer, QA, etc.)
- skills: JSON array of technical skills
- github_username: GitHub profile
- daily_work_hours: Work capacity
- timezone: User timezone
```

#### Task Model
```python
- id: Primary key
- title: Task title
- description: Detailed description
- task_type: Feature/Bug/Enhancement/etc.
- status: Backlog/Todo/In Progress/etc.
- priority: Critical/High/Medium/Low
- story_points: Agile estimation
- estimated_hours: Time estimation
- actual_hours: Time spent
- labels: JSON array of tags
- acceptance_criteria: Definition of done
- parent_task_id: For subtasks
- project_id: Associated project
- sprint_id: Current sprint
```

#### Project Model
```python
- id: Primary key
- name: Project name
- description: Project details
- status: Planning/Active/Completed/etc.
- repository_url: Git repository
- technology_stack: JSON array of technologies
- client_name: Client information
- estimated_hours: Project estimation
```

#### Sprint Model
```python
- id: Primary key
- name: Sprint name
- goal: Sprint objective
- start_date: Sprint start
- end_date: Sprint end
- capacity_hours: Team capacity
- velocity_points: Expected velocity
- status: Planned/Active/Completed
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Redis (for background tasks)

### Environment Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd task-management-backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
Create a `.env` file:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/task_management
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost:5432/task_management

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-flask-secret-key

# Redis Configuration (for background tasks)
REDIS_URL=redis://localhost:6379/0

# File Upload Configuration
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads/
```

5. **Database Setup**
```bash
# Initialize database
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

6. **Run the application**
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword",
  "role": "DEVELOPER"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword"
}
```

### Task Management Endpoints

#### Create Task
```http
POST /api/tasks
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication system",
  "task_type": "FEATURE",
  "priority": "HIGH",
  "story_points": 8,
  "estimated_hours": 16,
  "labels": ["backend", "security"],
  "acceptance_criteria": "Users can login and access protected routes",
  "project_id": 1,
  "assigned_to_id": 2,
  "due_date": "2024-02-15T10:00:00Z"
}
```

#### Get Tasks with Filters
```http
GET /api/tasks?project_id=1&status=IN_PROGRESS&assigned_to_id=2
Authorization: Bearer <jwt-token>
```

#### Update Task Status
```http
PUT /api/tasks/1
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "status": "IN_REVIEW",
  "actual_hours": 12
}
```

### Sprint Management Endpoints

#### Create Sprint
```http
POST /api/sprints
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "name": "Sprint 1 - Authentication Module",
  "description": "Implement core authentication features",
  "project_id": 1,
  "start_date": "2024-02-01T09:00:00Z",
  "end_date": "2024-02-14T17:00:00Z",
  "goal": "Complete user authentication system",
  "capacity_hours": 160,
  "velocity_points": 40
}
```

#### Start Sprint
```http
POST /api/sprints/1/start
Authorization: Bearer <jwt-token>
```

#### Get Sprint Burndown
```http
GET /api/sprints/1/burndown
Authorization: Bearer <jwt-token>
```

### Time Tracking Endpoints

#### Log Time
```http
POST /api/tasks/1/time
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "hours": 4.5,
  "description": "Implemented JWT token validation",
  "work_date": "2024-02-05"
}
```

### Project Management Endpoints

#### Create Project
```http
POST /api/projects
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "name": "E-commerce Platform",
  "description": "Modern e-commerce solution",
  "repository_url": "https://github.com/company/ecommerce",
  "technology_stack": ["Python", "Flask", "PostgreSQL", "React"],
  "client_name": "Tech Corp",
  "client_email": "contact@techcorp.com"
}
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Different permissions for different roles
- **Input Validation**: Comprehensive data validation
- **Rate Limiting**: API rate limiting to prevent abuse
- **CORS Configuration**: Secure cross-origin resource sharing
- **Password Hashing**: Bcrypt password hashing

## 📊 Analytics & Reporting

The system provides comprehensive analytics:

- **Task Analytics**: Completion rates, cycle times, burndown charts
- **Project Analytics**: Progress tracking, resource utilization
- **User Analytics**: Productivity metrics, workload distribution
- **Sprint Analytics**: Velocity tracking, sprint retrospectives

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_tasks.py
```

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
```

### Production Configuration
- Use PostgreSQL for production database
- Configure Redis for background tasks
- Set up proper logging
- Use environment variables for secrets
- Configure reverse proxy (Nginx)
- Set up SSL certificates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the API documentation at `/api/docs` (when running)
- Review the example requests in the `examples/` directory

## 🔄 Version History

- **v2.0.0** - Enhanced IT task management system
  - Added sprint management
  - Implemented time tracking
  - Enhanced user roles and permissions
  - Added project team management
  - Improved analytics and reporting

- **v1.0.0** - Initial release
  - Basic task management
  - User authentication
  - Simple project support