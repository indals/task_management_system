# Task Management System API Documentation

## Overview
This document provides comprehensive API documentation for the Flask-based Task Management System. The API follows RESTful conventions and uses JWT (JSON Web Tokens) for authentication.

**Base URL:** `http://localhost:5000` (development)  
**API Version:** v1  
**Authentication:** JWT Bearer Token

## Table of Contents
1. [Authentication](#authentication)
2. [Tasks](#tasks)
3. [Projects](#projects)
4. [Comments](#comments)
5. [Sprints](#sprints)
6. [Notifications](#notifications)
7. [Analytics](#analytics)
8. [Enums](#enums)
9. [Error Responses](#error-responses)
10. [Data Models](#data-models)

---

## Authentication

### Register User
**Endpoint:** `POST /api/auth/register`  
**Description:** Register a new user account  
**Authentication:** None required  

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "securePassword123",
  "role": "DEVELOPER"
}
```

**Response Example (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "role": "DEVELOPER",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**
- `400 Bad Request` - Missing required fields or invalid data
- `409 Conflict` - Email already exists

---

### Login User
**Endpoint:** `POST /api/auth/login`  
**Description:** Authenticate user and receive access token  
**Authentication:** None required  

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "john.doe@example.com",
  "password": "securePassword123"
}
```

**Response Example (200 OK):**
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "role": "DEVELOPER"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Missing email or password
- `401 Unauthorized` - Invalid credentials

---

### Get Current User
**Endpoint:** `GET /api/auth/me`  
**Description:** Get current authenticated user information  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "role": "DEVELOPER",
  "avatar_url": "https://example.com/avatar.jpg",
  "bio": "Full-stack developer with 5 years experience",
  "skills": ["JavaScript", "Python", "React", "Flask"],
  "timezone": "UTC",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### Update Profile
**Endpoint:** `PUT /api/auth/profile`  
**Description:** Update user profile information  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "John Smith",
  "bio": "Senior Full-stack Developer",
  "skills": ["JavaScript", "Python", "React", "Flask", "Docker"],
  "github_username": "johnsmith",
  "linkedin_url": "https://linkedin.com/in/johnsmith",
  "timezone": "America/New_York"
}
```

**Response Example (200 OK):**
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "name": "John Smith",
    "email": "john.doe@example.com",
    "bio": "Senior Full-stack Developer",
    "skills": ["JavaScript", "Python", "React", "Flask", "Docker"],
    "github_username": "johnsmith",
    "linkedin_url": "https://linkedin.com/in/johnsmith",
    "timezone": "America/New_York",
    "updated_at": "2024-01-15T11:45:00Z"
  }
}
```

---

### Change Password
**Endpoint:** `POST /api/auth/change-password`  
**Description:** Change user password  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "current_password": "oldPassword123",
  "new_password": "newSecurePassword456"
}
```

**Response Example (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

---

### Get All Users
**Endpoint:** `GET /api/auth/users`  
**Description:** Get list of all users (for task assignment)  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "role": "DEVELOPER"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane.smith@example.com",
      "role": "PROJECT_MANAGER"
    }
  ]
}
```

---

## Tasks

### Create Task
**Endpoint:** `POST /api/tasks`  
**Description:** Create a new task  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication system with login/register functionality",
  "priority": "HIGH",
  "task_type": "FEATURE",
  "project_id": 1,
  "assigned_to_id": 2,
  "due_date": "2024-02-01T17:00:00Z",
  "estimated_hours": 16.0,
  "story_points": 8,
  "labels": ["backend", "security"],
  "acceptance_criteria": "User can register, login, and access protected routes"
}
```

**Response Example (201 Created):**
```json
{
  "message": "Task created successfully",
  "task": {
    "id": 1,
    "title": "Implement user authentication",
    "description": "Add JWT-based authentication system with login/register functionality",
    "status": "BACKLOG",
    "priority": "HIGH",
    "task_type": "FEATURE",
    "project_id": 1,
    "assigned_to_id": 2,
    "created_by_id": 1,
    "due_date": "2024-02-01T17:00:00Z",
    "estimated_hours": 16.0,
    "actual_hours": 0.0,
    "story_points": 8,
    "labels": ["backend", "security"],
    "acceptance_criteria": "User can register, login, and access protected routes",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

---

### Get Tasks
**Endpoint:** `GET /api/tasks`  
**Description:** Get tasks with optional filtering  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `project_id` (integer, optional) - Filter by project ID
- `sprint_id` (integer, optional) - Filter by sprint ID
- `assigned_to_id` (integer, optional) - Filter by assigned user ID
- `created_by_id` (integer, optional) - Filter by creator user ID
- `status` (string, optional) - Filter by task status
- `priority` (string, optional) - Filter by task priority
- `task_type` (string, optional) - Filter by task type
- `overdue` (boolean, optional) - Filter overdue tasks
- `parent_task_id` (integer, optional) - Filter by parent task ID

**Example Request:**
```
GET /api/tasks?project_id=1&status=IN_PROGRESS&assigned_to_id=2
```

**Response Example (200 OK):**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Implement user authentication",
      "description": "Add JWT-based authentication system",
      "status": "IN_PROGRESS",
      "priority": "HIGH",
      "task_type": "FEATURE",
      "project": {
        "id": 1,
        "name": "Task Management System"
      },
      "assignee": {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane.smith@example.com"
      },
      "creator": {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com"
      },
      "due_date": "2024-02-01T17:00:00Z",
      "estimated_hours": 16.0,
      "actual_hours": 4.5,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-16T14:20:00Z"
    }
  ],
  "total": 1
}
```

---

### Get Task by ID
**Endpoint:** `GET /api/tasks/{task_id}`  
**Description:** Get a specific task by ID with comments  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `task_id` (integer, required) - Task ID

**Response Example (200 OK):**
```json
{
  "id": 1,
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication system",
  "status": "IN_PROGRESS",
  "priority": "HIGH",
  "task_type": "FEATURE",
  "project": {
    "id": 1,
    "name": "Task Management System"
  },
  "assignee": {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com"
  },
  "creator": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "due_date": "2024-02-01T17:00:00Z",
  "estimated_hours": 16.0,
  "actual_hours": 4.5,
  "story_points": 8,
  "labels": ["backend", "security"],
  "acceptance_criteria": "User can register, login, and access protected routes",
  "comments": [
    {
      "id": 1,
      "text": "Started working on the authentication endpoints",
      "author": {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane.smith@example.com"
      },
      "created_at": "2024-01-16T09:15:00Z"
    }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T14:20:00Z"
}
```

---

### Update Task
**Endpoint:** `PUT /api/tasks/{task_id}`  
**Description:** Update an existing task  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Path Parameters:**
- `task_id` (integer, required) - Task ID

**Request Body:**
```json
{
  "title": "Implement user authentication (Updated)",
  "status": "IN_PROGRESS",
  "priority": "CRITICAL",
  "actual_hours": 8.0,
  "completion_date": "2024-01-20T15:30:00Z"
}
```

**Response Example (200 OK):**
```json
{
  "message": "Task updated successfully",
  "task": {
    "id": 1,
    "title": "Implement user authentication (Updated)",
    "status": "IN_PROGRESS",
    "priority": "CRITICAL",
    "actual_hours": 8.0,
    "completion_date": "2024-01-20T15:30:00Z",
    "updated_at": "2024-01-20T15:30:00Z"
  }
}
```

---

### Delete Task
**Endpoint:** `DELETE /api/tasks/{task_id}`  
**Description:** Delete a task  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `task_id` (integer, required) - Task ID

**Response Example (200 OK):**
```json
{
  "message": "Task deleted successfully"
}
```

---

### Assign Task
**Endpoint:** `POST /api/tasks/{task_id}/assign`  
**Description:** Assign a task to a user  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Path Parameters:**
- `task_id` (integer, required) - Task ID

**Request Body:**
```json
{
  "user_id": 3
}
```

**Response Example (200 OK):**
```json
{
  "message": "Task assigned successfully",
  "task": {
    "id": 1,
    "title": "Implement user authentication",
    "assigned_to_id": 3,
    "assignee": {
      "id": 3,
      "name": "Bob Wilson",
      "email": "bob.wilson@example.com"
    }
  }
}
```

---

### Add Comment to Task
**Endpoint:** `POST /api/tasks/{task_id}/comments`  
**Description:** Add a comment to a task  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Path Parameters:**
- `task_id` (integer, required) - Task ID

**Request Body:**
```json
{
  "text": "I've completed the login endpoint and started working on registration"
}
```

**Response Example (201 Created):**
```json
{
  "message": "Comment added successfully",
  "comment": {
    "id": 2,
    "text": "I've completed the login endpoint and started working on registration",
    "task_id": 1,
    "user_id": 2,
    "author": {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane.smith@example.com"
    },
    "created_at": "2024-01-17T11:20:00Z"
  }
}
```

---

### Log Time on Task
**Endpoint:** `POST /api/tasks/{task_id}/time`  
**Description:** Log time spent on a task  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Path Parameters:**
- `task_id` (integer, required) - Task ID

**Request Body:**
```json
{
  "hours": 3.5,
  "description": "Implemented JWT authentication middleware",
  "work_date": "2024-01-17"
}
```

**Response Example (201 Created):**
```json
{
  "message": "Time logged successfully",
  "time_log": {
    "id": 1,
    "task_id": 1,
    "user_id": 2,
    "hours": 3.5,
    "description": "Implemented JWT authentication middleware",
    "work_date": "2024-01-17",
    "created_at": "2024-01-17T16:30:00Z"
  }
}
```

---

### Get Time Logs for Task
**Endpoint:** `GET /api/tasks/{task_id}/time`  
**Description:** Get time logs for a specific task  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `task_id` (integer, required) - Task ID

**Response Example (200 OK):**
```json
{
  "task": {
    "id": 1,
    "title": "Implement user authentication",
    "total_logged_hours": 12.5
  },
  "time_logs": [
    {
      "id": 1,
      "user_id": 2,
      "hours": 3.5,
      "description": "Implemented JWT authentication middleware",
      "work_date": "2024-01-17",
      "user": {
        "id": 2,
        "name": "Jane Smith"
      },
      "created_at": "2024-01-17T16:30:00Z"
    },
    {
      "id": 2,
      "user_id": 2,
      "hours": 4.0,
      "description": "Added user registration endpoint",
      "work_date": "2024-01-18",
      "user": {
        "id": 2,
        "name": "Jane Smith"
      },
      "created_at": "2024-01-18T17:00:00Z"
    }
  ],
  "total_hours": 12.5,
  "contributors": [
    {
      "user_id": 2,
      "name": "Jane Smith",
      "hours": 12.5
    }
  ]
}
```

---

### Get Overdue Tasks
**Endpoint:** `GET /api/tasks/overdue`  
**Description:** Get all overdue tasks for the current user  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "overdue_tasks": [
    {
      "id": 5,
      "title": "Fix login bug",
      "status": "IN_PROGRESS",
      "priority": "HIGH",
      "due_date": "2024-01-10T17:00:00Z",
      "days_overdue": 7,
      "project": {
        "id": 1,
        "name": "Task Management System"
      },
      "assignee": {
        "id": 2,
        "name": "Jane Smith"
      }
    }
  ],
  "total": 1
}
```

---

## Projects

### Create Project
**Endpoint:** `POST /api/projects`  
**Description:** Create a new project  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "E-commerce Platform",
  "description": "Modern e-commerce platform with React frontend and Flask backend",
  "technology_stack": ["React", "Flask", "PostgreSQL", "Redis"],
  "start_date": "2024-02-01T00:00:00Z",
  "end_date": "2024-06-30T23:59:59Z",
  "estimated_hours": 800.0,
  "client_name": "ABC Corporation",
  "client_email": "contact@abc-corp.com"
}
```

**Response Example (201 Created):**
```json
{
  "message": "Project created successfully",
  "project": {
    "id": 2,
    "name": "E-commerce Platform",
    "description": "Modern e-commerce platform with React frontend and Flask backend",
    "status": "PLANNING",
    "technology_stack": ["React", "Flask", "PostgreSQL", "Redis"],
    "start_date": "2024-02-01T00:00:00Z",
    "end_date": "2024-06-30T23:59:59Z",
    "estimated_hours": 800.0,
    "client_name": "ABC Corporation",
    "client_email": "contact@abc-corp.com",
    "owner_id": 1,
    "created_at": "2024-01-15T12:00:00Z"
  }
}
```

---

### Get All Projects
**Endpoint:** `GET /api/projects`  
**Description:** Get all projects  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "projects": [
    {
      "id": 1,
      "name": "Task Management System",
      "description": "Internal task management and collaboration tool",
      "status": "ACTIVE",
      "technology_stack": ["Flask", "React", "PostgreSQL"],
      "owner": {
        "id": 1,
        "name": "John Doe"
      },
      "team_size": 5,
      "task_count": 23,
      "created_at": "2024-01-01T00:00:00Z"
    },
    {
      "id": 2,
      "name": "E-commerce Platform",
      "description": "Modern e-commerce platform",
      "status": "PLANNING",
      "technology_stack": ["React", "Flask", "PostgreSQL", "Redis"],
      "owner": {
        "id": 1,
        "name": "John Doe"
      },
      "team_size": 0,
      "task_count": 0,
      "created_at": "2024-01-15T12:00:00Z"
    }
  ],
  "total": 2
}
```

---

### Get Project by ID
**Endpoint:** `GET /api/projects/{project_id}`  
**Description:** Get a specific project by ID  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `project_id` (integer, required) - Project ID

**Response Example (200 OK):**
```json
{
  "id": 1,
  "name": "Task Management System",
  "description": "Internal task management and collaboration tool",
  "status": "ACTIVE",
  "technology_stack": ["Flask", "React", "PostgreSQL"],
  "repository_url": "https://github.com/company/task-management",
  "documentation_url": "https://docs.company.com/task-management",
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-12-31T23:59:59Z",
  "estimated_hours": 2000.0,
  "owner": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "client_name": "Internal",
  "team_members": [
    {
      "id": 1,
      "name": "John Doe",
      "role": "PROJECT_MANAGER",
      "joined_at": "2024-01-01T00:00:00Z"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "role": "DEVELOPER",
      "joined_at": "2024-01-02T00:00:00Z"
    }
  ],
  "task_summary": {
    "total": 23,
    "completed": 8,
    "in_progress": 5,
    "pending": 10
  },
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### Update Project
**Endpoint:** `PATCH /api/projects/{project_id}`  
**Description:** Update project information  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Path Parameters:**
- `project_id` (integer, required) - Project ID

**Request Body:**
```json
{
  "status": "ACTIVE",
  "description": "Updated project description",
  "estimated_hours": 2200.0
}
```

**Response Example (200 OK):**
```json
{
  "message": "Project updated successfully",
  "project": {
    "id": 1,
    "name": "Task Management System",
    "description": "Updated project description",
    "status": "ACTIVE",
    "estimated_hours": 2200.0,
    "updated_at": "2024-01-17T14:30:00Z"
  }
}
```

---

### Delete Project
**Endpoint:** `DELETE /api/projects/{project_id}`  
**Description:** Delete a project  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `project_id` (integer, required) - Project ID

**Response Example (200 OK):**
```json
{
  "message": "Project deleted successfully"
}
```

---

### Get Recent Projects
**Endpoint:** `GET /api/projects/recent`  
**Description:** Get recently accessed projects  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "recent_projects": [
    {
      "id": 1,
      "name": "Task Management System",
      "status": "ACTIVE",
      "last_activity": "2024-01-17T14:30:00Z"
    },
    {
      "id": 2,
      "name": "E-commerce Platform",
      "status": "PLANNING",
      "last_activity": "2024-01-16T11:20:00Z"
    }
  ]
}
```

---

## Comments

### Get Task Comments
**Endpoint:** `GET /api/tasks/{task_id}/comments`  
**Description:** Get all comments for a specific task  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `task_id` (integer, required) - Task ID

**Response Example (200 OK):**
```json
{
  "comments": [
    {
      "id": 1,
      "text": "Started working on the authentication endpoints",
      "task_id": 1,
      "author": {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "avatar_url": "https://example.com/avatar2.jpg"
      },
      "created_at": "2024-01-16T09:15:00Z",
      "updated_at": "2024-01-16T09:15:00Z"
    },
    {
      "id": 2,
      "text": "I've completed the login endpoint and started working on registration",
      "task_id": 1,
      "author": {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "avatar_url": "https://example.com/avatar2.jpg"
      },
      "created_at": "2024-01-17T11:20:00Z",
      "updated_at": "2024-01-17T11:20:00Z"
    }
  ],
  "total": 2
}
```

---

### Update Comment
**Endpoint:** `PUT /api/tasks/comments/{comment_id}`  
**Description:** Update a comment (only by comment author)  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Path Parameters:**
- `comment_id` (integer, required) - Comment ID

**Request Body:**
```json
{
  "comment": "Updated comment text with more details about the implementation"
}
```

**Response Example (200 OK):**
```json
{
  "message": "Comment updated successfully",
  "comment": {
    "id": 2,
    "text": "Updated comment text with more details about the implementation",
    "updated_at": "2024-01-17T15:45:00Z"
  }
}
```

---

### Delete Comment
**Endpoint:** `DELETE /api/tasks/comments/{comment_id}`  
**Description:** Delete a comment (only by comment author)  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `comment_id` (integer, required) - Comment ID

**Response Example (200 OK):**
```json
{
  "message": "Comment deleted successfully"
}
```

---

## Sprints

### Create Sprint
**Endpoint:** `POST /api/sprints`  
**Description:** Create a new sprint for agile project management  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Sprint 1 - Authentication Module",
  "description": "Focus on implementing user authentication and security features",
  "project_id": 1,
  "start_date": "2024-02-01T09:00:00Z",
  "end_date": "2024-02-14T17:00:00Z",
  "goal": "Complete user authentication system with JWT tokens",
  "capacity_hours": 80.0,
  "velocity_points": 21
}
```

**Response Example (201 Created):**
```json
{
  "message": "Sprint created successfully",
  "sprint": {
    "id": 1,
    "name": "Sprint 1 - Authentication Module",
    "description": "Focus on implementing user authentication and security features",
    "status": "PLANNED",
    "project_id": 1,
    "start_date": "2024-02-01T09:00:00Z",
    "end_date": "2024-02-14T17:00:00Z",
    "goal": "Complete user authentication system with JWT tokens",
    "capacity_hours": 80.0,
    "velocity_points": 21,
    "tasks_count": 0,
    "created_at": "2024-01-15T12:00:00Z",
    "updated_at": "2024-01-15T12:00:00Z"
  }
}
```

---

### Get Sprint by ID
**Endpoint:** `GET /api/sprints/{sprint_id}`  
**Description:** Get a specific sprint by ID with optional task details  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `sprint_id` (integer, required) - Sprint ID

**Query Parameters:**
- `include_tasks` (boolean, optional) - Include sprint tasks in response

**Example Request:**
```
GET /api/sprints/1?include_tasks=true
```

**Response Example (200 OK):**
```json
{
  "id": 1,
  "name": "Sprint 1 - Authentication Module",
  "description": "Focus on implementing user authentication and security features",
  "status": "ACTIVE",
  "project_id": 1,
  "project": {
    "id": 1,
    "name": "Task Management System"
  },
  "start_date": "2024-02-01T09:00:00Z",
  "end_date": "2024-02-14T17:00:00Z",
  "goal": "Complete user authentication system with JWT tokens",
  "capacity_hours": 80.0,
  "velocity_points": 21,
  "tasks": [
    {
      "id": 1,
      "title": "Implement user authentication",
      "status": "IN_PROGRESS",
      "priority": "HIGH",
      "story_points": 8,
      "assignee": {
        "id": 2,
        "name": "Jane Smith"
      }
    }
  ],
  "tasks_count": 5,
  "completed_tasks": 2,
  "remaining_points": 13,
  "created_at": "2024-01-15T12:00:00Z",
  "updated_at": "2024-02-01T09:00:00Z"
}
```

---

### Update Sprint
**Endpoint:** `PUT /api/sprints/{sprint_id}`  
**Description:** Update sprint information  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Path Parameters:**
- `sprint_id` (integer, required) - Sprint ID

**Request Body:**
```json
{
  "name": "Sprint 1 - Authentication & Security Module",
  "description": "Updated description with security focus",
  "goal": "Complete authentication system with enhanced security features",
  "capacity_hours": 90.0
}
```

**Response Example (200 OK):**
```json
{
  "message": "Sprint updated successfully",
  "sprint": {
    "id": 1,
    "name": "Sprint 1 - Authentication & Security Module",
    "description": "Updated description with security focus",
    "goal": "Complete authentication system with enhanced security features",
    "capacity_hours": 90.0,
    "updated_at": "2024-02-02T10:30:00Z"
  }
}
```

---

### Delete Sprint
**Endpoint:** `DELETE /api/sprints/{sprint_id}`  
**Description:** Delete a sprint  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `sprint_id` (integer, required) - Sprint ID

**Response Example (200 OK):**
```json
{
  "message": "Sprint deleted successfully"
}
```

---

### Get Project Sprints
**Endpoint:** `GET /api/sprints/project/{project_id}`  
**Description:** Get all sprints for a specific project  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `project_id` (integer, required) - Project ID

**Response Example (200 OK):**
```json
{
  "sprints": [
    {
      "id": 1,
      "name": "Sprint 1 - Authentication Module",
      "status": "COMPLETED",
      "start_date": "2024-02-01T09:00:00Z",
      "end_date": "2024-02-14T17:00:00Z",
      "tasks_count": 5,
      "completed_tasks": 5,
      "velocity_points": 21
    },
    {
      "id": 2,
      "name": "Sprint 2 - Task Management",
      "status": "ACTIVE",
      "start_date": "2024-02-15T09:00:00Z",
      "end_date": "2024-02-28T17:00:00Z",
      "tasks_count": 7,
      "completed_tasks": 3,
      "velocity_points": 28
    }
  ],
  "total": 2
}
```

---

### Start Sprint
**Endpoint:** `POST /api/sprints/{sprint_id}/start`  
**Description:** Start a planned sprint  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `sprint_id` (integer, required) - Sprint ID

**Response Example (200 OK):**
```json
{
  "message": "Sprint started successfully",
  "sprint": {
    "id": 1,
    "name": "Sprint 1 - Authentication Module",
    "status": "ACTIVE",
    "started_at": "2024-02-01T09:00:00Z"
  }
}
```

---

### Complete Sprint
**Endpoint:** `POST /api/sprints/{sprint_id}/complete`  
**Description:** Complete an active sprint  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `sprint_id` (integer, required) - Sprint ID

**Response Example (200 OK):**
```json
{
  "message": "Sprint completed successfully",
  "sprint": {
    "id": 1,
    "name": "Sprint 1 - Authentication Module",
    "status": "COMPLETED",
    "completed_at": "2024-02-14T17:00:00Z",
    "velocity_achieved": 21,
    "completion_rate": 100
  }
}
```

---

### Get Sprint Burndown Chart
**Endpoint:** `GET /api/sprints/{sprint_id}/burndown`  
**Description:** Get burndown chart data for sprint progress tracking  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `sprint_id` (integer, required) - Sprint ID

**Response Example (200 OK):**
```json
{
  "sprint": {
    "id": 1,
    "name": "Sprint 1 - Authentication Module",
    "start_date": "2024-02-01T09:00:00Z",
    "end_date": "2024-02-14T17:00:00Z",
    "total_points": 21
  },
  "burndown_data": [
    {
      "date": "2024-02-01",
      "remaining_points": 21,
      "ideal_remaining": 21,
      "completed_points": 0
    },
    {
      "date": "2024-02-02",
      "remaining_points": 18,
      "ideal_remaining": 19.5,
      "completed_points": 3
    },
    {
      "date": "2024-02-05",
      "remaining_points": 13,
      "ideal_remaining": 15.75,
      "completed_points": 8
    }
  ],
  "completion_rate": 62,
  "velocity": 8,
  "days_remaining": 7
}
```

---

### Add Task to Sprint
**Endpoint:** `POST /api/sprints/{sprint_id}/tasks/{task_id}`  
**Description:** Add a task to a sprint  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `sprint_id` (integer, required) - Sprint ID
- `task_id` (integer, required) - Task ID

**Response Example (200 OK):**
```json
{
  "message": "Task added to sprint successfully",
  "task": {
    "id": 5,
    "title": "Implement password reset functionality",
    "sprint_id": 1,
    "story_points": 5
  }
}
```

---

### Remove Task from Sprint
**Endpoint:** `DELETE /api/sprints/{sprint_id}/tasks/{task_id}`  
**Description:** Remove a task from a sprint  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `sprint_id` (integer, required) - Sprint ID
- `task_id` (integer, required) - Task ID

**Response Example (200 OK):**
```json
{
  "message": "Task removed from sprint successfully"
}
```

---

## Notifications

### Get User Notifications
**Endpoint:** `GET /api/notifications`  
**Description:** Get notifications for the authenticated user  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `unread_only` (boolean, optional) - Get only unread notifications

**Example Request:**
```
GET /api/notifications?unread_only=true
```

**Response Example (200 OK):**
```json
{
  "notifications": [
    {
      "id": 1,
      "type": "TASK_ASSIGNED",
      "title": "New Task Assigned",
      "message": "You have been assigned to task: Implement user authentication",
      "task_id": 1,
      "task": {
        "id": 1,
        "title": "Implement user authentication",
        "priority": "HIGH"
      },
      "related_user": {
        "id": 3,
        "name": "Bob Wilson",
        "email": "bob.wilson@example.com"
      },
      "project_id": 1,
      "read": false,
      "created_at": "2024-01-17T10:30:00Z"
    },
    {
      "id": 2,
      "type": "COMMENT_ADDED",
      "title": "New Comment on Task",
      "message": "Jane Smith commented on: Fix login bug",
      "task_id": 5,
      "related_user_id": 2,
      "read": false,
      "created_at": "2024-01-17T14:20:00Z"
    }
  ],
  "total": 2,
  "unread_count": 2
}
```

---

### Mark Notification as Read
**Endpoint:** `POST /api/notifications/{notification_id}/read`  
**Description:** Mark a specific notification as read  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `notification_id` (integer, required) - Notification ID

**Response Example (200 OK):**
```json
{
  "message": "Notification marked as read",
  "notification": {
    "id": 1,
    "read": true,
    "read_at": "2024-01-17T16:45:00Z"
  }
}
```

---

### Mark All Notifications as Read
**Endpoint:** `POST /api/notifications/read-all`  
**Description:** Mark all notifications as read for the authenticated user  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "message": "All notifications marked as read",
  "updated_count": 5
}
```

---

### Delete Notification
**Endpoint:** `DELETE /api/notifications/{notification_id}`  
**Description:** Delete a specific notification  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `notification_id` (integer, required) - Notification ID

**Response Example (200 OK):**
```json
{
  "message": "Notification deleted successfully"
}
```

---

## Analytics

### Get Task Completion Analytics
**Endpoint:** `GET /api/analytics/task-completion`  
**Description:** Get task completion rate analytics for performance tracking  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `user_id` (integer, optional) - Specific user ID (admin only)
- `period` (string, optional) - Time period: 'week', 'month', 'year' (default: 'month')

**Example Request:**
```
GET /api/analytics/task-completion?period=month&user_id=2
```

**Response Example (200 OK):**
```json
{
  "user": {
    "id": 2,
    "name": "Jane Smith"
  },
  "period": "month",
  "completion_rate": 85.5,
  "total_tasks": 23,
  "completed_tasks": 20,
  "in_progress_tasks": 2,
  "overdue_tasks": 1,
  "average_completion_time": 2.5,
  "productivity_trend": "increasing",
  "daily_breakdown": [
    {
      "date": "2024-01-01",
      "completed": 2,
      "created": 3
    },
    {
      "date": "2024-01-02",
      "completed": 1,
      "created": 2
    }
  ]
}
```

---

### Get User Productivity Analytics
**Endpoint:** `GET /api/analytics/user-productivity`  
**Description:** Get detailed user productivity metrics  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `user_id` (integer, optional) - Specific user ID (defaults to current user)

**Response Example (200 OK):**
```json
{
  "user": {
    "id": 2,
    "name": "Jane Smith",
    "role": "DEVELOPER"
  },
  "performance_metrics": {
    "total_tasks_completed": 45,
    "average_task_completion_time": 2.3,
    "on_time_completion_rate": 92.5,
    "total_hours_logged": 180.5,
    "average_daily_hours": 7.2,
    "efficiency_score": 88.7
  },
  "monthly_stats": {
    "tasks_completed": 12,
    "hours_worked": 85.5,
    "projects_contributed": 3,
    "comments_made": 28
  },
  "task_type_breakdown": {
    "FEATURE": 18,
    "BUG": 15,
    "ENHANCEMENT": 8,
    "REFACTOR": 4
  },
  "priority_handling": {
    "CRITICAL": 3,
    "HIGH": 12,
    "MEDIUM": 20,
    "LOW": 10
  }
}
```

---

### Get Task Status Distribution
**Endpoint:** `GET /api/analytics/task-status-distribution`  
**Description:** Get distribution of tasks by status across the system  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "total_tasks": 156,
  "status_distribution": {
    "BACKLOG": {
      "count": 25,
      "percentage": 16.0
    },
    "TODO": {
      "count": 18,
      "percentage": 11.5
    },
    "IN_PROGRESS": {
      "count": 32,
      "percentage": 20.5
    },
    "IN_REVIEW": {
      "count": 12,
      "percentage": 7.7
    },
    "TESTING": {
      "count": 8,
      "percentage": 5.1
    },
    "DONE": {
      "count": 55,
      "percentage": 35.3
    },
    "BLOCKED": {
      "count": 4,
      "percentage": 2.6
    },
    "CANCELLED": {
      "count": 2,
      "percentage": 1.3
    }
  },
  "completion_rate": 35.3,
  "active_tasks": 70
}
```

---

### Get Task Priority Distribution
**Endpoint:** `GET /api/analytics/task-priority-distribution`  
**Description:** Get distribution of tasks by priority levels  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "total_tasks": 156,
  "priority_distribution": {
    "CRITICAL": {
      "count": 8,
      "percentage": 5.1,
      "avg_completion_time": 1.2
    },
    "HIGH": {
      "count": 35,
      "percentage": 22.4,
      "avg_completion_time": 2.1
    },
    "MEDIUM": {
      "count": 78,
      "percentage": 50.0,
      "avg_completion_time": 3.5
    },
    "LOW": {
      "count": 35,
      "percentage": 22.4,
      "avg_completion_time": 5.2
    }
  },
  "high_priority_completion_rate": 89.5,
  "overdue_by_priority": {
    "CRITICAL": 0,
    "HIGH": 2,
    "MEDIUM": 5,
    "LOW": 8
  }
}
```

---

## Enums

### Get All Enums
**Endpoint:** `GET /api/enums`  
**Description:** Get all enum values for dropdowns and validation  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "UserRole": {
    "ADMIN": "ADMIN",
    "PROJECT_MANAGER": "PROJECT_MANAGER",
    "TEAM_LEAD": "TEAM_LEAD",
    "SENIOR_DEVELOPER": "SENIOR_DEVELOPER",
    "DEVELOPER": "DEVELOPER",
    "QA_ENGINEER": "QA_ENGINEER",
    "DEVOPS_ENGINEER": "DEVOPS_ENGINEER",
    "UI_UX_DESIGNER": "UI_UX_DESIGNER",
    "BUSINESS_ANALYST": "BUSINESS_ANALYST",
    "PRODUCT_OWNER": "PRODUCT_OWNER",
    "SCRUM_MASTER": "SCRUM_MASTER"
  },
  "TaskStatus": {
    "BACKLOG": "BACKLOG",
    "TODO": "TODO",
    "IN_PROGRESS": "IN_PROGRESS",
    "IN_REVIEW": "IN_REVIEW",
    "TESTING": "TESTING",
    "BLOCKED": "BLOCKED",
    "DONE": "DONE",
    "CANCELLED": "CANCELLED",
    "DEPLOYED": "DEPLOYED"
  },
  "TaskPriority": {
    "CRITICAL": "CRITICAL",
    "HIGH": "HIGH",
    "MEDIUM": "MEDIUM",
    "LOW": "LOW"
  },
  "TaskType": {
    "FEATURE": "FEATURE",
    "BUG": "BUG",
    "ENHANCEMENT": "ENHANCEMENT",
    "REFACTOR": "REFACTOR",
    "DOCUMENTATION": "DOCUMENTATION",
    "TESTING": "TESTING",
    "DEPLOYMENT": "DEPLOYMENT",
    "RESEARCH": "RESEARCH",
    "MAINTENANCE": "MAINTENANCE",
    "SECURITY": "SECURITY"
  },
  "ProjectStatus": {
    "PLANNING": "PLANNING",
    "ACTIVE": "ACTIVE",
    "ON_HOLD": "ON_HOLD",
    "COMPLETED": "COMPLETED",
    "CANCELLED": "CANCELLED"
  },
  "SprintStatus": {
    "PLANNED": "PLANNED",
    "ACTIVE": "ACTIVE",
    "COMPLETED": "COMPLETED",
    "CANCELLED": "CANCELLED"
  },
  "NotificationType": {
    "TASK_ASSIGNED": "TASK_ASSIGNED",
    "TASK_UPDATED": "TASK_UPDATED",
    "TASK_COMPLETED": "TASK_COMPLETED",
    "TASK_OVERDUE": "TASK_OVERDUE",
    "COMMENT_ADDED": "COMMENT_ADDED",
    "PROJECT_UPDATED": "PROJECT_UPDATED",
    "SPRINT_STARTED": "SPRINT_STARTED",
    "SPRINT_COMPLETED": "SPRINT_COMPLETED",
    "MENTION": "MENTION"
  },
  "EstimationUnit": {
    "HOURS": "HOURS",
    "DAYS": "DAYS",
    "STORY_POINTS": "STORY_POINTS"
  }
}
```

---

### Get User Roles
**Endpoint:** `GET /api/enums/user-roles`  
**Description:** Get available user role options  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "ADMIN": "ADMIN",
  "PROJECT_MANAGER": "PROJECT_MANAGER",
  "TEAM_LEAD": "TEAM_LEAD",
  "SENIOR_DEVELOPER": "SENIOR_DEVELOPER",
  "DEVELOPER": "DEVELOPER",
  "QA_ENGINEER": "QA_ENGINEER",
  "DEVOPS_ENGINEER": "DEVOPS_ENGINEER",
  "UI_UX_DESIGNER": "UI_UX_DESIGNER",
  "BUSINESS_ANALYST": "BUSINESS_ANALYST",
  "PRODUCT_OWNER": "PRODUCT_OWNER",
  "SCRUM_MASTER": "SCRUM_MASTER"
}
```

---

### Get Task Statuses
**Endpoint:** `GET /api/enums/task-statuses`  
**Description:** Get available task status options  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "BACKLOG": "BACKLOG",
  "TODO": "TODO",
  "IN_PROGRESS": "IN_PROGRESS",
  "IN_REVIEW": "IN_REVIEW",
  "TESTING": "TESTING",
  "BLOCKED": "BLOCKED",
  "DONE": "DONE",
  "CANCELLED": "CANCELLED",
  "DEPLOYED": "DEPLOYED"
}
```

---

### Get Task Priorities
**Endpoint:** `GET /api/enums/task-priorities`  
**Description:** Get available task priority options  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "CRITICAL": "CRITICAL",
  "HIGH": "HIGH",
  "MEDIUM": "MEDIUM",
  "LOW": "LOW"
}
```

---

### Get Task Types
**Endpoint:** `GET /api/enums/task-types`  
**Description:** Get available task type options  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "FEATURE": "FEATURE",
  "BUG": "BUG",
  "ENHANCEMENT": "ENHANCEMENT",
  "REFACTOR": "REFACTOR",
  "DOCUMENTATION": "DOCUMENTATION",
  "TESTING": "TESTING",
  "DEPLOYMENT": "DEPLOYMENT",
  "RESEARCH": "RESEARCH",
  "MAINTENANCE": "MAINTENANCE",
  "SECURITY": "SECURITY"
}
```

---

### Get Project Statuses
**Endpoint:** `GET /api/enums/project-statuses`  
**Description:** Get available project status options  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "PLANNING": "PLANNING",
  "ACTIVE": "ACTIVE",
  "ON_HOLD": "ON_HOLD",
  "COMPLETED": "COMPLETED",
  "CANCELLED": "CANCELLED"
}
```

---

### Get Sprint Statuses
**Endpoint:** `GET /api/enums/sprint-statuses`  
**Description:** Get available sprint status options  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "PLANNED": "PLANNED",
  "ACTIVE": "ACTIVE",
  "COMPLETED": "COMPLETED",
  "CANCELLED": "CANCELLED"
}
```

---

## Error Responses

### Standard Error Format
All error responses follow this format:

```json
{
  "error": "Error message describing what went wrong",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional error details if applicable"
  }
}
```

### Common HTTP Status Codes

**400 Bad Request**
```json
{
  "error": "Missing required fields",
  "details": {
    "missing_fields": ["title", "project_id"]
  }
}
```

**401 Unauthorized**
```json
{
  "error": "Authentication required",
  "code": "UNAUTHORIZED"
}
```

**403 Forbidden**
```json
{
  "error": "You don't have permission to perform this action",
  "code": "FORBIDDEN"
}
```

**404 Not Found**
```json
{
  "error": "Task not found",
  "code": "NOT_FOUND"
}
```

**409 Conflict**
```json
{
  "error": "Email already exists",
  "code": "CONFLICT"
}
```

**422 Unprocessable Entity**
```json
{
  "error": "Validation failed",
  "details": {
    "email": "Invalid email format",
    "password": "Password must be at least 8 characters"
  }
}
```

**500 Internal Server Error**
```json
{
  "error": "An internal server error occurred",
  "code": "INTERNAL_ERROR"
}
```

---

## Data Models

### User Model
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "role": "DEVELOPER",
  "avatar_url": "https://example.com/avatar.jpg",
  "bio": "Full-stack developer with 5 years experience",
  "skills": ["JavaScript", "Python", "React", "Flask"],
  "github_username": "johndoe",
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "phone": "+1-555-0123",
  "timezone": "America/New_York",
  "daily_work_hours": 8.0,
  "hourly_rate": 75.0,
  "is_active": true,
  "last_login": "2024-01-17T09:30:00Z",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-17T09:30:00Z"
}
```

### Task Model
```json
{
  "id": 1,
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication system",
  "status": "IN_PROGRESS",
  "priority": "HIGH",
  "task_type": "FEATURE",
  "project_id": 1,
  "sprint_id": 2,
  "assigned_to_id": 2,
  "created_by_id": 1,
  "parent_task_id": null,
  "due_date": "2024-02-01T17:00:00Z",
  "start_date": "2024-01-15T09:00:00Z",
  "completion_date": null,
  "estimated_hours": 16.0,
  "actual_hours": 4.5,
  "story_points": 8,
  "estimation_unit": "HOURS",
  "labels": ["backend", "security"],
  "acceptance_criteria": "User can register, login, and access protected routes",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T14:20:00Z"
}
```

### Project Model
```json
{
  "id": 1,
  "name": "Task Management System",
  "description": "Internal task management and collaboration tool",
  "status": "ACTIVE",
  "repository_url": "https://github.com/company/task-management",
  "documentation_url": "https://docs.company.com/task-management",
  "technology_stack": ["Flask", "React", "PostgreSQL"],
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-12-31T23:59:59Z",
  "estimated_hours": 2000.0,
  "owner_id": 1,
  "client_name": "Internal",
  "client_email": "internal@company.com",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Comment Model
```json
{
  "id": 1,
  "text": "Started working on the authentication endpoints",
  "task_id": 1,
  "user_id": 2,
  "created_at": "2024-01-16T09:15:00Z",
  "updated_at": "2024-01-16T09:15:00Z"
}
```

### Time Log Model
```json
{
  "id": 1,
  "task_id": 1,
  "user_id": 2,
  "hours": 3.5,
  "description": "Implemented JWT authentication middleware",
  "work_date": "2024-01-17",
  "created_at": "2024-01-17T16:30:00Z"
}
```

### Sprint Model
```json
{
  "id": 1,
  "name": "Sprint 1 - Authentication Module",
  "description": "Focus on implementing user authentication and security features",
  "status": "ACTIVE",
  "project_id": 1,
  "start_date": "2024-02-01T09:00:00Z",
  "end_date": "2024-02-14T17:00:00Z",
  "goal": "Complete user authentication system with JWT tokens",
  "capacity_hours": 80.0,
  "velocity_points": 21,
  "created_at": "2024-01-15T12:00:00Z",
  "updated_at": "2024-02-01T09:00:00Z"
}
```

### Notification Model
```json
{
  "id": 1,
  "user_id": 2,
  "task_id": 1,
  "type": "TASK_ASSIGNED",
  "title": "New Task Assigned",
  "message": "You have been assigned to task: Implement user authentication",
  "related_user_id": 3,
  "project_id": 1,
  "sprint_id": null,
  "read": false,
  "read_at": null,
  "created_at": "2024-01-17T10:30:00Z"
}
```

---

## Authentication

### JWT Token Format
The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Token Payload
```json
{
  "user_id": 1,
  "email": "john.doe@example.com",
  "role": "DEVELOPER",
  "exp": 1705507200,
  "iat": 1705420800
}
```

### Token Expiration
- Access tokens expire after 24 hours
- Refresh tokens expire after 30 days
- Include the token in all protected endpoints

---

## Rate Limiting
- 1000 requests per hour per user for authenticated endpoints
- 100 requests per hour per IP for authentication endpoints
- Rate limit headers are included in responses:
  - `X-RateLimit-Limit`: Request limit per hour
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Unix timestamp when limit resets

---

## Pagination
For endpoints that return lists, pagination is supported:

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `per_page` (integer, default: 20, max: 100) - Items per page

**Response Format:**
```json
{
  "items": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "pages": 8,
    "has_next": true,
    "has_prev": false,
    "next_page": 2,
    "prev_page": null
  }
}
```

---

## Webhooks
The system supports webhooks for real-time notifications:

**Supported Events:**
- `task.created`
- `task.updated`
- `task.assigned`
- `task.completed`
- `comment.added`
- `project.created`
- `project.updated`

**Webhook Payload Example:**
```json
{
  "event": "task.created",
  "timestamp": "2024-01-17T10:30:00Z",
  "data": {
    "task": {...},
    "user": {...}
  }
}
```

---

This documentation covers all the main endpoints and features of your Flask Task Management System API. Each endpoint includes detailed request/response examples, authentication requirements, and error handling information.