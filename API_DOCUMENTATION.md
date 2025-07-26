# Task Management System API Documentation

## Overview
This document provides comprehensive API documentation for the Flask-based Task Management System. The API follows RESTful conventions and uses JWT (JSON Web Tokens) for authentication.

**Base URL:** `http://localhost:5000` (development)  
**Production URL:** `http://65.2.186.248:5000`  
**API Version:** v1  
**Authentication:** JWT Bearer Token

## Table of Contents
1. [Authentication](#authentication)
2. [Tasks](#tasks)
3. [Projects](#projects)
4. [Sprints](#sprints)
5. [Comments](#comments)
6. [Notifications](#notifications)
7. [Analytics](#analytics)
8. [Time Logs](#time-logs)
9. [Enums](#enums)
10. [Error Responses](#error-responses)
11. [Data Models](#data-models)

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
    "avatar_url": null,
    "bio": null,
    "skills": [],
    "github_username": null,
    "linkedin_url": null,
    "timezone": "UTC",
    "daily_work_hours": 8.0,
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
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
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "role": "DEVELOPER",
    "avatar_url": null,
    "bio": null,
    "skills": [],
    "github_username": null,
    "linkedin_url": null,
    "timezone": "UTC",
    "daily_work_hours": 8.0,
    "hourly_rate": null,
    "is_active": true,
    "last_login": "2024-01-15T10:30:00Z"
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
  "email": "john.smith@example.com",
  "bio": "Senior Full-stack Developer",
  "skills": ["JavaScript", "Python", "React", "Flask", "Docker"],
  "github_username": "johnsmith",
  "linkedin_url": "https://linkedin.com/in/johnsmith",
  "phone": "+1-555-0123",
  "timezone": "America/New_York",
  "daily_work_hours": 8.5,
  "hourly_rate": 80.0
}
```

**Response Example (200 OK):**
```json
{
  "message": "Profile updated successfully"
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
  "message": "Password changed successfully",
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "role": "DEVELOPER"
}
```

---

### Get All Users
**Endpoint:** `GET /api/auth/users`  
**Description:** Get list of all users for task assignment  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "role": "DEVELOPER"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "role": "PROJECT_MANAGER"
  }
]
```

---

### Test Endpoint
**Endpoint:** `GET /api/auth/ping`  
**Description:** Test if authentication API is working  
**Authentication:** None required  

**Response Example (200 OK):**
```json
{
  "message": "Auth API is working!"
}
```

---

## Tasks

### Create Task
**Endpoint:** `POST /api/tasks`  
**Description:** Create a new task with enhanced features  
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
  "status": "BACKLOG",
  "project_id": 1,
  "sprint_id": null,
  "assigned_to_id": 2,
  "due_date": "2024-02-01T17:00:00Z",
  "start_date": "2024-01-15T09:00:00Z",
  "estimated_hours": 16.0,
  "story_points": 8,
  "estimation_unit": "HOURS",
  "labels": ["backend", "security"],
  "acceptance_criteria": "User can register, login, and access protected routes",
  "parent_task_id": null
}
```

**Response Example (201 Created):**
```json
{
  "id": 1,
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication system with login/register functionality",
  "status": "BACKLOG",
  "priority": "HIGH",
  "task_type": "FEATURE",
  "assigned_to": {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "role": "DEVELOPER"
  },
  "created_by": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "role": "PROJECT_MANAGER"
  },
  "project": {
    "id": 1,
    "name": "Task Management System"
  },
  "sprint": null,
  "due_date": "2024-02-01T17:00:00Z",
  "start_date": "2024-01-15T09:00:00Z",
  "completion_date": null,
  "estimated_hours": 16.0,
  "actual_hours": 0.0,
  "story_points": 8,
  "estimation_unit": "HOURS",
  "labels": ["backend", "security"],
  "acceptance_criteria": "User can register, login, and access protected routes",
  "parent_task_id": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "comments_count": 0,
  "attachments_count": 0,
  "time_logs_count": 0
}
```

---

### Get Tasks
**Endpoint:** `GET /api/tasks`  
**Description:** Get tasks with advanced filtering  
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
[
  {
    "id": 1,
    "title": "Implement user authentication",
    "description": "Add JWT-based authentication system",
    "status": "IN_PROGRESS",
    "priority": "HIGH",
    "task_type": "FEATURE",
    "assigned_to": {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane.smith@example.com",
      "role": "DEVELOPER"
    },
    "created_by": {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "role": "PROJECT_MANAGER"
    },
    "project": {
      "id": 1,
      "name": "Task Management System"
    },
    "sprint": {
      "id": 2,
      "name": "Sprint 2 - Authentication"
    },
    "due_date": "2024-02-01T17:00:00Z",
    "start_date": "2024-01-15T09:00:00Z",
    "completion_date": null,
    "estimated_hours": 16.0,
    "actual_hours": 4.5,
    "story_points": 8,
    "estimation_unit": "HOURS",
    "labels": ["backend", "security"],
    "acceptance_criteria": "User can register, login, and access protected routes",
    "parent_task_id": null,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-16T14:20:00Z",
    "comments_count": 2,
    "attachments_count": 0,
    "time_logs_count": 3
  }
]
```

---

### Get Overdue Tasks
**Endpoint:** `GET /api/tasks/overdue`  
**Description:** Get overdue tasks for the current user  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
[
  {
    "id": 5,
    "title": "Fix login bug",
    "status": "IN_PROGRESS",
    "priority": "HIGH",
    "due_date": "2024-01-10T17:00:00Z",
    "assigned_to": {
      "id": 2,
      "name": "Jane Smith"
    },
    "project": {
      "id": 1,
      "name": "Task Management System"
    }
  }
]
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
  "assigned_to": {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "role": "DEVELOPER"
  },
  "created_by": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "role": "PROJECT_MANAGER"
  },
  "project": {
    "id": 1,
    "name": "Task Management System"
  },
  "sprint": {
    "id": 2,
    "name": "Sprint 2 - Authentication"
  },
  "due_date": "2024-02-01T17:00:00Z",
  "start_date": "2024-01-15T09:00:00Z",
  "completion_date": null,
  "estimated_hours": 16.0,
  "actual_hours": 4.5,
  "story_points": 8,
  "estimation_unit": "HOURS",
  "labels": ["backend", "security"],
  "acceptance_criteria": "User can register, login, and access protected routes",
  "parent_task_id": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T14:20:00Z",
  "comments_count": 2,
  "attachments_count": 0,
  "time_logs_count": 3,
  "comments": [
    {
      "id": 1,
      "comment": "Started working on the authentication endpoints",
      "user_id": 2,
      "created_at": "2024-01-16T09:15:00Z",
      "updated_at": "2024-01-16T09:15:00Z",
      "author": {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane.smith@example.com"
      }
    }
  ]
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
  "completion_date": "2024-01-20T15:30:00Z",
  "labels": ["backend", "security", "urgent"]
}
```

**Response Example (200 OK):**
```json
{
  "id": 1,
  "title": "Implement user authentication (Updated)",
  "status": "IN_PROGRESS",
  "priority": "CRITICAL",
  "actual_hours": 8.0,
  "completion_date": "2024-01-20T15:30:00Z",
  "labels": ["backend", "security", "urgent"],
  "updated_at": "2024-01-20T15:30:00Z"
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
  "message": "Task deleted successfully",
  "task_id": 1
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
  "id": 1,
  "title": "Implement user authentication",
  "assigned_to": {
    "id": 3,
    "name": "Bob Wilson",
    "email": "bob.wilson@example.com",
    "role": "SENIOR_DEVELOPER"
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
  "id": 2,
  "text": "I've completed the login endpoint and started working on registration",
  "author": {
    "id": 2,
    "name": "Jane Smith"
  },
  "createdAt": "2024-01-17T11:20:00Z"
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
  "id": 1,
  "task_id": 1,
  "user_id": 2,
  "hours": 3.5,
  "description": "Implemented JWT authentication middleware",
  "work_date": "2024-01-17",
  "logged_at": "2024-01-17T16:30:00Z",
  "updated_at": "2024-01-17T16:30:00Z",
  "task": {
    "id": 1,
    "title": "Implement user authentication"
  },
  "user": {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com"
  },
  "hours_formatted": "3h 30m"
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
[
  {
    "id": 1,
    "task_id": 1,
    "user_id": 2,
    "hours": 3.5,
    "description": "Implemented JWT authentication middleware",
    "work_date": "2024-01-17",
    "logged_at": "2024-01-17T16:30:00Z",
    "updated_at": "2024-01-17T16:30:00Z",
    "task": {
      "id": 1,
      "title": "Implement user authentication"
    },
    "user": {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane.smith@example.com"
    },
    "hours_formatted": "3h 30m"
  }
]
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
  "status": "PLANNING",
  "repository_url": "https://github.com/company/ecommerce",
  "documentation_url": "https://docs.company.com/ecommerce",
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
  "id": 2,
  "name": "E-commerce Platform",
  "description": "Modern e-commerce platform with React frontend and Flask backend",
  "status": "PLANNING",
  "repository_url": "https://github.com/company/ecommerce",
  "documentation_url": "https://docs.company.com/ecommerce",
  "technology_stack": ["React", "Flask", "PostgreSQL", "Redis"],
  "start_date": "2024-02-01T00:00:00Z",
  "end_date": "2024-06-30T23:59:59Z",
  "estimated_hours": 800.0,
  "client_name": "ABC Corporation",
  "client_email": "contact@abc-corp.com",
  "owner": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "tasks_count": 0,
  "created_at": "2024-01-15T12:00:00Z",
  "updated_at": "2024-01-15T12:00:00Z"
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
  "tasks_count": 5,
  "created_at": "2024-01-15T12:00:00Z",
  "updated_at": "2024-02-01T09:00:00Z",
  "tasks": [
    {
      "id": 1,
      "title": "Implement user authentication",
      "status": "IN_PROGRESS",
      "priority": "HIGH",
      "story_points": 8,
      "assigned_to": {
        "id": 2,
        "name": "Jane Smith"
      }
    }
  ]
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
  "capacity_hours": 90.0,
  "status": "ACTIVE"
}
```

**Response Example (200 OK):**
```json
{
  "id": 1,
  "name": "Sprint 1 - Authentication & Security Module",
  "description": "Updated description with security focus",
  "goal": "Complete authentication system with enhanced security features",
  "capacity_hours": 90.0,
  "status": "ACTIVE",
  "updated_at": "2024-02-02T10:30:00Z"
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
[
  {
    "id": 1,
    "name": "Sprint 1 - Authentication Module",
    "status": "COMPLETED",
    "start_date": "2024-02-01T09:00:00Z",
    "end_date": "2024-02-14T17:00:00Z",
    "tasks_count": 5,
    "velocity_points": 21,
    "created_at": "2024-01-15T12:00:00Z",
    "updated_at": "2024-02-14T17:00:00Z"
  },
  {
    "id": 2,
    "name": "Sprint 2 - Task Management",
    "status": "ACTIVE",
    "start_date": "2024-02-15T09:00:00Z",
    "end_date": "2024-02-28T17:00:00Z",
    "tasks_count": 7,
    "velocity_points": 28,
    "created_at": "2024-02-01T12:00:00Z",
    "updated_at": "2024-02-15T09:00:00Z"
  }
]
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
  "id": 1,
  "name": "Sprint 1 - Authentication Module",
  "status": "ACTIVE",
  "start_date": "2024-02-01T09:00:00Z",
  "updated_at": "2024-02-01T09:00:00Z"
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
  "id": 1,
  "name": "Sprint 1 - Authentication Module",
  "status": "COMPLETED",
  "end_date": "2024-02-14T17:00:00Z",
  "velocity_points": 21,
  "updated_at": "2024-02-14T17:00:00Z"
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
  "total_points": 21,
  "completed_points": 13,
  "remaining_points": 8,
  "completion_percentage": 61.9
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
  "id": 5,
  "title": "Implement password reset functionality",
  "sprint_id": 1,
  "story_points": 5,
  "status": "TODO"
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
  "id": 5,
  "title": "Implement password reset functionality",
  "sprint_id": null,
  "status": "BACKLOG"
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
[
  {
    "id": 1,
    "task_id": 1,
    "user_id": 2,
    "comment": "Started working on the authentication endpoints",
    "created_at": "2024-01-16T09:15:00Z",
    "updated_at": "2024-01-16T09:15:00Z",
    "user": {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane.smith@example.com",
      "role": "DEVELOPER",
      "avatar_url": "https://example.com/avatar2.jpg"
    }
  },
  {
    "id": 2,
    "task_id": 1,
    "user_id": 2,
    "comment": "I've completed the login endpoint and started working on registration",
    "created_at": "2024-01-17T11:20:00Z",
    "updated_at": "2024-01-17T11:20:00Z",
    "user": {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane.smith@example.com",
      "role": "DEVELOPER",
      "avatar_url": "https://example.com/avatar2.jpg"
    }
  }
]
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
  "id": 2,
  "comment": "Updated comment text with more details about the implementation",
  "updated_at": "2024-01-17T15:45:00Z"
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
[
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
    "created_at": "2024-01-17T10:30:00Z",
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
    "project": {
      "id": 1,
      "name": "Task Management System"
    }
  },
  {
    "id": 2,
    "user_id": 2,
    "task_id": 5,
    "type": "COMMENT_ADDED",
    "title": "New Comment on Task",
    "message": "Jane Smith commented on: Fix login bug",
    "related_user_id": 2,
    "project_id": 1,
    "sprint_id": null,
    "read": false,
    "read_at": null,
    "created_at": "2024-01-17T14:20:00Z"
  }
]
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
  "id": 1,
  "read": true,
  "read_at": "2024-01-17T16:45:00Z"
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
  "message": "All notifications marked as read"
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
  "time_period": "month",
  "total_tasks": 23,
  "completed_tasks": 20,
  "completion_rate": 0.87,
  "start_date": "2023-12-17T10:30:00Z",
  "end_date": "2024-01-17T10:30:00Z"
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
  "total_tasks": 45,
  "completed_tasks": 40,
  "completion_rate": 0.89
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
  "BACKLOG": 25,
  "TODO": 18,
  "IN_PROGRESS": 32,
  "IN_REVIEW": 12,
  "TESTING": 8,
  "DONE": 55,
  "BLOCKED": 4,
  "CANCELLED": 2
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
  "CRITICAL": 8,
  "HIGH": 35,
  "MEDIUM": 78,
  "LOW": 35
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

## Health Check

### Database Health Check
**Endpoint:** `GET /api/health/db`  
**Description:** Check database connection status  
**Authentication:** None required  

**Response Example (200 OK):**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "status": "unhealthy",
  "error": "Connection timeout"
}
```

---

### General Health Check
**Endpoint:** `GET /api/health`  
**Description:** General service health check  
**Authentication:** None required  

**Response Example (200 OK):**
```json
{
  "status": "healthy",
  "service": "task-management-api"
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

**Schema:**
- `id` (integer) - Primary key
- `name` (string, max 100) - User's full name
- `email` (string, max 120, unique) - User's email address
- `role` (enum) - User role (see UserRole enum)
- `avatar_url` (string, max 500, nullable) - Profile picture URL
- `bio` (text, nullable) - User biography
- `skills` (JSON array, nullable) - List of technical skills
- `github_username` (string, max 100, nullable) - GitHub username
- `linkedin_url` (string, max 500, nullable) - LinkedIn profile URL
- `phone` (string, max 20, nullable) - Phone number
- `timezone` (string, max 50, default "UTC") - User timezone
- `daily_work_hours` (float, default 8.0) - Expected daily work hours
- `hourly_rate` (float, nullable) - Hourly billing rate
- `is_active` (boolean, default true) - Account status
- `last_login` (datetime, nullable) - Last login timestamp
- `created_at` (datetime) - Account creation timestamp
- `updated_at` (datetime) - Last update timestamp

---

### Task Model
```json
{
  "id": 1,
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication system",
  "status": "IN_PROGRESS",
  "priority": "HIGH",
  "task_type": "FEATURE",
  "assigned_to": {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com"
  },
  "created_by": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "project": {
    "id": 1,
    "name": "Task Management System"
  },
  "sprint": {
    "id": 2,
    "name": "Sprint 2 - Authentication"
  },
  "due_date": "2024-02-01T17:00:00Z",
  "start_date": "2024-01-15T09:00:00Z",
  "completion_date": null,
  "estimated_hours": 16.0,
  "actual_hours": 4.5,
  "story_points": 8,
  "estimation_unit": "HOURS",
  "labels": ["backend", "security"],
  "acceptance_criteria": "User can register, login, and access protected routes",
  "parent_task_id": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T14:20:00Z",
  "comments_count": 2,
  "attachments_count": 0,
  "time_logs_count": 3
}
```

**Schema:**
- `id` (integer) - Primary key
- `title` (string, max 200) - Task title
- `description` (text, nullable) - Detailed description
- `status` (enum) - Task status (see TaskStatus enum)
- `priority` (enum) - Task priority (see TaskPriority enum)
- `task_type` (enum) - Task type (see TaskType enum)
- `assigned_to_id` (integer, nullable) - Assigned user ID
- `created_by_id` (integer) - Creator user ID
- `project_id` (integer, nullable) - Associated project ID
- `sprint_id` (integer, nullable) - Associated sprint ID
- `due_date` (datetime, nullable) - Due date
- `start_date` (datetime, nullable) - Start date
- `completion_date` (datetime, nullable) - Completion date
- `estimated_hours` (float, nullable) - Estimated hours
- `actual_hours` (float, default 0.0) - Actual hours spent
- `story_points` (integer, nullable) - Agile story points
- `estimation_unit` (enum, default "HOURS") - Unit of estimation
- `labels` (JSON array, nullable) - Task labels/tags
- `acceptance_criteria` (text, nullable) - Definition of done
- `parent_task_id` (integer, nullable) - Parent task for subtasks
- `created_at` (datetime) - Creation timestamp
- `updated_at` (datetime) - Last update timestamp

---

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
  "owner": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "client_name": "Internal",
  "client_email": "internal@company.com",
  "tasks_count": 23,
  "sprints_count": 3,
  "team_members_count": 5,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Schema:**
- `id` (integer) - Primary key
- `name` (string, max 200) - Project name
- `description` (text, nullable) - Project description
- `status` (enum) - Project status (see ProjectStatus enum)
- `repository_url` (string, max 500, nullable) - Git repository URL
- `documentation_url` (string, max 500, nullable) - Documentation URL
- `technology_stack` (JSON array, nullable) - Technologies used
- `start_date` (datetime, nullable) - Project start date
- `end_date` (datetime, nullable) - Project end date
- `estimated_hours` (float, nullable) - Total estimated hours
- `owner_id` (integer) - Project owner user ID
- `client_name` (string, max 200, nullable) - Client name
- `client_email` (string, max 120, nullable) - Client email
- `created_at` (datetime) - Creation timestamp
- `updated_at` (datetime) - Last update timestamp

---

### Sprint Model
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
  "tasks_count": 5,
  "created_at": "2024-01-15T12:00:00Z",
  "updated_at": "2024-02-01T09:00:00Z"
}
```

**Schema:**
- `id` (integer) - Primary key
- `name` (string, max 200) - Sprint name
- `description` (text, nullable) - Sprint description
- `status` (enum) - Sprint status (see SprintStatus enum)
- `project_id` (integer) - Associated project ID
- `start_date` (datetime) - Sprint start date
- `end_date` (datetime) - Sprint end date
- `goal` (text, nullable) - Sprint goal
- `capacity_hours` (float, nullable) - Team capacity in hours
- `velocity_points` (integer, nullable) - Expected velocity points
- `created_at` (datetime) - Creation timestamp
- `updated_at` (datetime) - Last update timestamp

---

### Comment Model
```json
{
  "id": 1,
  "task_id": 1,
  "user_id": 2,
  "comment": "Started working on the authentication endpoints",
  "created_at": "2024-01-16T09:15:00Z",
  "updated_at": "2024-01-16T09:15:00Z",
  "user": {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "role": "DEVELOPER"
  }
}
```

**Schema:**
- `id` (integer) - Primary key
- `task_id` (integer) - Associated task ID
- `user_id` (integer) - Comment author user ID
- `comment` (text) - Comment text
- `created_at` (datetime) - Creation timestamp
- `updated_at` (datetime) - Last update timestamp

---

### Time Log Model
```json
{
  "id": 1,
  "task_id": 1,
  "user_id": 2,
  "hours": 3.5,
  "description": "Implemented JWT authentication middleware",
  "work_date": "2024-01-17",
  "logged_at": "2024-01-17T16:30:00Z",
  "updated_at": "2024-01-17T16:30:00Z",
  "task": {
    "id": 1,
    "title": "Implement user authentication"
  },
  "user": {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com"
  },
  "hours_formatted": "3h 30m"
}
```

**Schema:**
- `id` (integer) - Primary key
- `task_id` (integer) - Associated task ID
- `user_id` (integer) - User who logged time
- `hours` (float) - Hours worked
- `description` (text, nullable) - Work description
- `work_date` (date) - Date of work
- `logged_at` (datetime) - When time was logged
- `updated_at` (datetime) - Last update timestamp

---

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

**Schema:**
- `id` (integer) - Primary key
- `user_id` (integer) - Recipient user ID
- `task_id` (integer, nullable) - Related task ID
- `type` (enum) - Notification type (see NotificationType enum)
- `title` (string, max 200) - Notification title
- `message` (text) - Notification message
- `related_user_id` (integer, nullable) - User who triggered notification
- `project_id` (integer, nullable) - Related project ID
- `sprint_id` (integer, nullable) - Related sprint ID
- `read` (boolean, default false) - Read status
- `read_at` (datetime, nullable) - When marked as read
- `created_at` (datetime) - Creation timestamp

---

### Project Member Model
```json
{
  "id": 1,
  "project_id": 1,
  "user_id": 2,
  "role": "Lead Developer",
  "can_create_tasks": true,
  "can_edit_tasks": true,
  "can_delete_tasks": false,
  "can_manage_sprints": true,
  "can_manage_members": false,
  "joined_at": "2024-01-02T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z",
  "project": {
    "id": 1,
    "name": "Task Management System"
  },
  "user": {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "role": "DEVELOPER"
  }
}
```

**Schema:**
- `id` (integer) - Primary key
- `project_id` (integer) - Project ID
- `user_id` (integer) - User ID
- `role` (string, max 100, nullable) - Role in project
- `can_create_tasks` (boolean, default true) - Task creation permission
- `can_edit_tasks` (boolean, default true) - Task editing permission
- `can_delete_tasks` (boolean, default false) - Task deletion permission
- `can_manage_sprints` (boolean, default false) - Sprint management permission
- `can_manage_members` (boolean, default false) - Member management permission
- `joined_at` (datetime) - When user joined project
- `updated_at` (datetime) - Last update timestamp

---

### Task Attachment Model
```json
{
  "id": 1,
  "task_id": 1,
  "uploaded_by_id": 2,
  "filename": "auth_diagram_20240117.png",
  "original_filename": "authentication_flow_diagram.png",
  "file_path": "/uploads/tasks/1/auth_diagram_20240117.png",
  "file_size": 245760,
  "mime_type": "image/png",
  "uploaded_at": "2024-01-17T14:30:00Z",
  "uploaded_by": {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com"
  },
  "file_size_formatted": "240.0 KB"
}
```

**Schema:**
- `id` (integer) - Primary key
- `task_id` (integer) - Associated task ID
- `uploaded_by_id` (integer) - Uploader user ID
- `filename` (string, max 255) - Stored filename
- `original_filename` (string, max 255) - Original filename
- `file_path` (string, max 500) - File storage path
- `file_size` (integer, nullable) - File size in bytes
- `mime_type` (string, max 100, nullable) - MIME type
- `uploaded_at` (datetime) - Upload timestamp

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

## File Upload
For endpoints that support file uploads:

**Supported File Types:**
- Images: JPG, JPEG, PNG, GIF, BMP, WEBP, SVG
- Documents: PDF, DOC, DOCX, TXT, RTF, ODT
- Code Files: PY, JS, HTML, CSS, JAVA, CPP, C, PHP, RB, GO, RS, TS, JSX, VUE, SQL, JSON, XML, YAML, YML

**File Size Limits:**
- Maximum file size: 16MB
- Multiple files can be uploaded per task

**Request Format:**
```
Content-Type: multipart/form-data
```

---

## CORS Configuration
The API supports Cross-Origin Resource Sharing (CORS) with the following configuration:
- Allowed Origins: `*` (all origins for development)
- Allowed Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
- Allowed Headers: Content-Type, Authorization
- Supports Credentials: Yes

---

## Database Configuration
**Development:**
- Database: PostgreSQL
- Host: dev-database.c1qe2o6s6oix.ap-south-1.rds.amazonaws.com
- Port: 5432
- Database Name: myapp

**Connection Pooling:**
- Pool Size: 5 connections
- Pool Timeout: 20 seconds
- Pool Recycle: 300 seconds (5 minutes)
- Pool Pre-ping: Enabled

---

## Environment Variables
Required environment variables for configuration:

```bash
# Database
DATABASE_URL=postgresql://username:password@host:port/database
SQLALCHEMY_DATABASE_URI=postgresql://username:password@host:port/database

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-flask-secret-key

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# File Upload
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads/
```

---

## Deployment
The API can be deployed using:

### Docker
```bash
docker build -t task-management-api .
docker run -p 5000:5000 task-management-api
```

### Docker Compose
```bash
docker-compose up -d
```

### Manual Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
flask db upgrade

# Start with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app
```

### GitHub Actions CI/CD
The repository includes automated deployment to EC2 via GitHub Actions:
- Triggers on push to master branch
- Deploys to EC2 instance at 65.2.186.248:5000
- Includes health checks and rollback capabilities

---

## Security Features
- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **Input Validation**: Comprehensive data validation on all endpoints
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **CORS Configuration**: Secure cross-origin resource sharing
- **Rate Limiting**: Prevents API abuse
- **Role-Based Access Control**: Different permissions for different user roles

---

## Monitoring & Health Checks
- **Health Check Endpoints**: `/api/health` and `/api/health/db`
- **Database Connection Monitoring**: Automatic connection validation
- **Error Logging**: Comprehensive error logging and tracking
- **Performance Monitoring**: Database query optimization and monitoring

---

## Testing
The API includes comprehensive test coverage:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_tasks.py
```

**Test Categories:**
- Unit tests for models and services
- Integration tests for API endpoints
- Authentication and authorization tests
- Database transaction tests

---

## API Versioning
Current API version: **v1**

Future versions will be accessible via:
- URL versioning: `/api/v2/tasks`
- Header versioning: `Accept: application/vnd.api+json;version=2`

---

## Support & Documentation
- **API Documentation**: This document
- **Interactive API Explorer**: Available at `/api/docs` (when running)
- **GitHub Repository**: Complete source code and examples
- **Issue Tracking**: GitHub Issues for bug reports and feature requests

---

## Changelog

### Version 2.0.0 (Current)
- Enhanced IT task management system
- Added sprint management functionality
- Implemented comprehensive time tracking
- Enhanced user roles and permissions
- Added project team management
- Improved analytics and reporting
- Added file attachment support
- Enhanced notification system

### Version 1.0.0
- Initial release
- Basic task management
- User authentication
- Simple project support
- Basic CRUD operations

---

This documentation covers all available endpoints, request/response formats, authentication requirements, and detailed schema information for the Task Management System API. For additional support or questions, please refer to the GitHub repository or contact the development team.
  "sprints_count": 0,
  "team_members_count": 0,
  "created_at": "2024-01-15T12:00:00Z",
  "updated_at": "2024-01-15T12:00:00Z"
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
[
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
    "client_name": "Internal",
    "client_email": "internal@company.com",
    "owner": {
      "id": 1,
      "name": "John Doe"
    },
    "tasks_count": 23,
    "sprints_count": 3,
    "team_members_count": 5,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
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
  "repository_url": "https://github.com/company/task-management",
  "documentation_url": "https://docs.company.com/task-management",
  "technology_stack": ["Flask", "React", "PostgreSQL"],
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-12-31T23:59:59Z",
  "estimated_hours": 2000.0,
  "client_name": "Internal",
  "client_email": "internal@company.com",
  "owner": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "tasks_count": 23,
  "sprints_count": 3,
  "team_members_count": 5,
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
  "name": "Updated Project Name",
  "status": "ACTIVE",
  "description": "Updated project description",
  "estimated_hours": 2200.0
}
```

**Response Example (200 OK):**
```json
{
  "id": 1,
  "name": "Updated Project Name",
  "description": "Updated project description",
  "status": "ACTIVE",
  "estimated_hours": 2200.0,
  "updated_at": "2024-01-17T14:30:00Z"
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
[
  {
    "id": 1,
    "name": "Task Management System",
    "description": "Internal task management and collaboration tool",
    "status": "ACTIVE",
    "owner": {
      "id": 1,
      "name": "John Doe"
    },
    "tasks_count": 23,
    "sprints_count": 3,
    "team_members_count": 5,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-17T14:30:00Z"
  }
]
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
  "id": 1,
  "name": "Sprint 1 - Authentication Module",
  "description": "Focus on implementing user authentication and security features",
  "status": "PLANNED",
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
  "tasks_count": 0,