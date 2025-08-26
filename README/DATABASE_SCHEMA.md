# Task Management System - Database Schema Documentation

## Overview
This document describes the database schema for a comprehensive task management system built with SQLAlchemy. The system supports project-based task management with features like sprint planning, time tracking, notifications, and team collaboration.

## 📊 Database Tables Overview

### Core Entities
- **Users** - System users with different roles
- **Projects** - Main containers for organizing work
- **Tasks** - Individual work items within projects
- **Sprints** - Time-boxed iterations for agile development

### Supporting Entities
- **Project Members** - User-project associations with permissions
- **Task Comments** - Comments and discussions on tasks
- **Task Attachments** - File uploads attached to tasks
- **Time Logs** - Time tracking entries for tasks
- **Notifications** - System notifications for users

---

## 🗃️ Detailed Table Schemas

### 1. Users Table
**Purpose**: Stores user accounts and profile information

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer (PK) | Unique user identifier |
| `name` | String(100) | User's full name |
| `email` | String(120) | Email address (unique) |
| `password_hash` | String(200) | Encrypted password |
| `role` | Enum | User role (ADMIN, DEVELOPER, etc.) |
| `avatar_url` | String(500) | Profile picture URL |
| `bio` | Text | User biography |
| `skills` | Text | JSON array of skills |
| `github_username` | String(100) | GitHub username |
| `linkedin_url` | String(500) | LinkedIn profile URL |
| `phone` | String(20) | Phone number |
| `timezone` | String(50) | User's timezone |
| `daily_work_hours` | Float | Expected daily work hours |
| `hourly_rate` | Float | Billing rate per hour |
| `is_active` | Boolean | Account status |
| `last_login` | DateTime | Last login timestamp |
| `created_at` | DateTime | Account creation time |
| `updated_at` | DateTime | Last profile update |

**Available Roles**:
- ADMIN, PROJECT_MANAGER, TEAM_LEAD
- SENIOR_DEVELOPER, DEVELOPER, QA_ENGINEER
- DEVOPS_ENGINEER, UI_UX_DESIGNER
- BUSINESS_ANALYST, PRODUCT_OWNER, SCRUM_MASTER

---

### 2. Projects Table
**Purpose**: Main containers for organizing tasks and team collaboration

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer (PK) | Unique project identifier |
| `name` | String(200) | Project name |
| `description` | Text | Project description |
| `status` | Enum | Project status (PLANNING, ACTIVE, etc.) |
| `repository_url` | String(500) | Git repository URL |
| `documentation_url` | String(500) | Documentation link |
| `technology_stack` | Text | JSON array of technologies |
| `start_date` | DateTime | Project start date |
| `end_date` | DateTime | Project end date |
| `estimated_hours` | Float | Total estimated hours |
| `owner_id` | Integer (FK) | References `users.id` |
| `client_name` | String(200) | Client/customer name |
| `client_email` | String(120) | Client contact email |
| `created_at` | DateTime | Project creation time |
| `updated_at` | DateTime | Last update time |

**Available Statuses**: PLANNING, ACTIVE, ON_HOLD, COMPLETED, CANCELLED

---

### 3. Tasks Table
**Purpose**: Individual work items within projects

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer (PK) | Unique task identifier |
| `title` | String(200) | Task title |
| `description` | Text | Detailed description |
| `status` | Enum | Current status |
| `priority` | Enum | Task priority level |
| `task_type` | Enum | Type of task |
| `assigned_to_id` | Integer (FK) | References `users.id` |
| `created_by_id` | Integer (FK) | References `users.id` |
| `project_id` | Integer (FK) | References `projects.id` |
| `sprint_id` | Integer (FK) | References `sprints.id` |
| `due_date` | DateTime | Task deadline |
| `start_date` | DateTime | Task start date |
| `completion_date` | DateTime | When task was completed |
| `estimated_hours` | Float | Estimated work hours |
| `actual_hours` | Float | Actual hours worked |
| `story_points` | Integer | Agile story points |
| `estimation_unit` | Enum | Unit for estimation |
| `labels` | Text | JSON array of labels |
| `acceptance_criteria` | Text | Definition of done |
| `parent_task_id` | Integer (FK) | References `tasks.id` (for subtasks) |
| `created_at` | DateTime | Task creation time |
| `updated_at` | DateTime | Last update time |

**Task Statuses**: BACKLOG, TODO, IN_PROGRESS, IN_REVIEW, TESTING, BLOCKED, DONE, CANCELLED, DEPLOYED

**Task Priorities**: CRITICAL, HIGH, MEDIUM, LOW

**Task Types**: FEATURE, BUG, ENHANCEMENT, REFACTOR, DOCUMENTATION, TESTING, DEPLOYMENT, RESEARCH, MAINTENANCE, SECURITY

**Estimation Units**: HOURS, DAYS, STORY_POINTS

---

### 4. Sprints Table
**Purpose**: Time-boxed iterations for agile project management

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer (PK) | Unique sprint identifier |
| `name` | String(200) | Sprint name |
| `description` | Text | Sprint description |
| `status` | Enum | Sprint status |
| `project_id` | Integer (FK) | References `projects.id` |
| `start_date` | DateTime | Sprint start date |
| `end_date` | DateTime | Sprint end date |
| `goal` | Text | Sprint goal/objective |
| `capacity_hours` | Float | Team capacity in hours |
| `velocity_points` | Integer | Planned story points |
| `created_at` | DateTime | Sprint creation time |
| `updated_at` | DateTime | Last update time |

**Sprint Statuses**: PLANNED, ACTIVE, COMPLETED, CANCELLED

---

### 5. Project Members Table
**Purpose**: Associates users with projects and defines their permissions

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer (PK) | Unique membership identifier |
| `project_id` | Integer (FK) | References `projects.id` |
| `user_id` | Integer (FK) | References `users.id` |
| `role` | String(100) | Role in this project |
| `can_create_tasks` | Boolean | Permission to create tasks |
| `can_edit_tasks` | Boolean | Permission to edit tasks |
| `can_delete_tasks` | Boolean | Permission to delete tasks |
| `can_manage_sprints` | Boolean | Permission to manage sprints |
| `can_manage_members` | Boolean | Permission to manage team |
| `joined_at` | DateTime | When user joined project |
| `updated_at` | DateTime | Last permission update |

**Unique Constraint**: (project_id, user_id) - prevents duplicate memberships

---

### 6. Task Comments Table
**Purpose**: Comments and discussions on tasks

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer (PK) | Unique comment identifier |
| `task_id` | Integer (FK) | References `tasks.id` |
| `user_id` | Integer (FK) | References `users.id` |
| `comment` | Text | Comment content |
| `created_at` | DateTime | Comment creation time |
| `updated_at` | DateTime | Last edit time |

---

### 7. Task Attachments Table
**Purpose**: File uploads associated with tasks

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer (PK) | Unique attachment identifier |
| `task_id` | Integer (FK) | References `tasks.id` |
| `uploaded_by_id` | Integer (FK) | References `users.id` |
| `filename` | String(255) | Generated filename |
| `original_filename` | String(255) | Original filename |
| `file_path` | String(500) | File storage path |
| `file_size` | Integer | File size in bytes |
| `mime_type` | String(100) | File MIME type |
| `uploaded_at` | DateTime | Upload timestamp |

---

### 8. Time Logs Table
**Purpose**: Time tracking entries for tasks

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer (PK) | Unique log identifier |
| `task_id` | Integer (FK) | References `tasks.id` |
| `user_id` | Integer (FK) | References `users.id` |
| `hours` | Float | Hours worked |
| `description` | Text | Work description |
| `work_date` | Date | Date work was performed |
| `logged_at` | DateTime | When entry was created |
| `updated_at` | DateTime | Last update time |

---

### 9. Notifications Table
**Purpose**: System notifications for users

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer (PK) | Unique notification identifier |
| `user_id` | Integer (FK) | References `users.id` |
| `task_id` | Integer (FK) | References `tasks.id` (optional) |
| `type` | Enum | Notification type |
| `title` | String(200) | Notification title |
| `message` | Text | Notification message |
| `related_user_id` | Integer (FK) | References `users.id` (trigger user) |
| `project_id` | Integer (FK) | References `projects.id` (optional) |
| `sprint_id` | Integer (FK) | References `sprints.id` (optional) |
| `read` | Boolean | Read status |
| `read_at` | DateTime | When notification was read |
| `created_at` | DateTime | Notification creation time |

**Notification Types**: TASK_ASSIGNED, TASK_UPDATED, TASK_COMPLETED, TASK_OVERDUE, COMMENT_ADDED, PROJECT_UPDATED, SPRINT_STARTED, SPRINT_COMPLETED, MENTION

---

## 🔗 Relationship Mapping

### User Relationships
```
User (1) ←→ (Many) Tasks [assigned_to]
User (1) ←→ (Many) Tasks [created_by]
User (1) ←→ (Many) Projects [owner]
User (1) ←→ (Many) ProjectMembers
User (1) ←→ (Many) TaskComments
User (1) ←→ (Many) TaskAttachments [uploaded_by]
User (1) ←→ (Many) TimeLogs
User (1) ←→ (Many) Notifications
```

### Project Relationships
```
Project (1) ←→ (Many) Tasks
Project (1) ←→ (Many) Sprints
Project (1) ←→ (Many) ProjectMembers
Project (1) ←→ (1) User [owner]
```

### Task Relationships
```
Task (1) ←→ (Many) TaskComments
Task (1) ←→ (Many) TaskAttachments
Task (1) ←→ (Many) TimeLogs
Task (1) ←→ (Many) Notifications
Task (1) ←→ (1) User [assignee]
Task (1) ←→ (1) User [creator]
Task (1) ←→ (1) Project
Task (1) ←→ (1) Sprint [optional]
Task (1) ←→ (1) Task [parent, for subtasks]
Task (1) ←→ (Many) Tasks [subtasks]
```

### Sprint Relationships
```
Sprint (1) ←→ (Many) Tasks
Sprint (1) ←→ (1) Project
```

---

## 🔄 Data Flow Examples

### Creating a New Task
1. User creates task in a project
2. Task record created with `created_by_id` and `project_id`
3. If assigned, `assigned_to_id` is set
4. Notification created for assignee
5. Task appears in project's task list

### Adding Team Member to Project
1. Project owner adds user to project
2. ProjectMember record created with permissions
3. User can now view/interact with project based on permissions
4. User appears in project's team member list

### Time Logging Workflow
1. User works on assigned task
2. User logs time with hours and description
3. TimeLog record created linked to task and user
4. Task's `actual_hours` updated automatically
5. Time appears in project reports and user timesheets

### Sprint Planning
1. Project manager creates sprint for project
2. Tasks are assigned to sprint (`sprint_id` updated)
3. Sprint appears in project's sprint list
4. Team members can view sprint backlog and burndown

---

## 🔐 Security Considerations

### Foreign Key Constraints
- All foreign keys use `CASCADE` delete for child records
- `SET NULL` used where record should remain but reference is removed
- Prevents orphaned records and maintains data integrity

### User Permissions
- Project-level permissions controlled via ProjectMember table
- Cascading deletes ensure cleanup when users/projects are removed
- Role-based access control via User.role enum

### Data Validation
- Unique constraints prevent duplicate emails and project memberships
- Enum types ensure data consistency
- NOT NULL constraints on required fields

---

## 📈 Performance Considerations

### Indexing Strategy
- Primary keys automatically indexed
- Foreign keys should be indexed for join performance
- Consider composite indexes for common query patterns:
  - `(project_id, status)` on tasks table
  - `(user_id, read)` on notifications table
  - `(user_id, work_date)` on time_logs table

### Query Optimization
- Use `back_populates` for bidirectional relationships
- Lazy loading by default, use `joinedload` for eager loading
- Consider pagination for large result sets

---

## 🚀 Getting Started

### Database Setup
```python
from app import db
from app.models import *

# Create all tables
db.create_all()

# Create admin user
admin = User.register(
    name="Admin User",
    email="admin@example.com", 
    password="secure_password",
    role=UserRole.ADMIN
)
```

### Sample Data Creation
```python
# Create a project
project = Project(
    name="Task Management System",
    description="A comprehensive task management solution",
    status=ProjectStatus.ACTIVE,
    owner_id=admin.id
)
db.session.add(project)
db.session.commit()

# Create a task
task = Task(
    title="Implement user authentication",
    description="Add login/logout functionality",
    status=TaskStatus.TODO,
    priority=TaskPriority.HIGH,
    task_type=TaskType.FEATURE,
    project_id=project.id,
    created_by_id=admin.id
)
db.session.add(task)
db.session.commit()
```

This schema provides a robust foundation for a full-featured task management system with support for agile workflows, team collaboration, and comprehensive tracking capabilities.