# Task Management System API Documentation (Updated)

## Overview
This document provides comprehensive API documentation for the Flask-based Task Management System. The API follows RESTful conventions and uses JWT (JSON Web Tokens) for authentication.

**Base URL:** `http://localhost:5000` (development)  
**Production URL:** `http://65.2.186.248:5000`  
**API Version:** v1  
**Authentication:** JWT Bearer Token

## Standardized Response Format

All API endpoints return responses in a consistent format:

### Success Response Structure
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    // Actual response data here
  },
  "timestamp": "2024-01-17T10:30:00.123456"
}
```

### Error Response Structure
```json
{
  "success": false,
  "message": "Error description",
  "data": null,
  "timestamp": "2024-01-17T10:30:00.123456"
}
```

### Common HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

---

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
10. [Health Check](#health-check)

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
  "success": true,
  "message": "User registered successfully",
  "data": {
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
  },
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "message": "Missing required fields",
  "data": null,
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

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
  "success": true,
  "message": "Login successful",
  "data": {
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
  },
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "success": false,
  "message": "Invalid credentials",
  "data": null,
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

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
  "success": true,
  "message": "User profile retrieved successfully",
  "data": {
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
  },
  "timestamp": "2024-01-17T09:30:00.123456"
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
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "id": 1,
    "name": "John Smith",
    "email": "john.smith@example.com"
  },
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "Password changed successfully",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "role": "DEVELOPER"
  },
  "timestamp": "2024-01-17T10:30:00.123456"
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
{
  "success": true,
  "message": "Users retrieved successfully",
  "data": [
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
  ],
  "timestamp": "2024-01-17T10:30:00.123456"
}
```

---

### Test Endpoint
**Endpoint:** `GET /api/auth/ping`  
**Description:** Test if authentication API is working  
**Authentication:** None required  

**Response Example (200 OK):**
```json
{
  "success": true,
  "message": "Auth API is working!",
  "data": null,
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "assigneeId": 2,
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
  "success": true,
  "message": "Task created successfully",
  "data": {
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
  },
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

---

### Get Tasks
**Endpoint:** `GET /api/tasks`  
**Description:** Get tasks with advanced filtering and pagination  
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
- `page` (integer, optional, default: 1) - Page number
- `per_page` (integer, optional, default: 10) - Items per page
- `sort_by` (string, optional, default: created_at) - Sort field
- `sort_order` (string, optional, default: desc) - Sort order

**Example Request:**
```
GET /api/tasks?project_id=1&status=IN_PROGRESS&assigned_to_id=2&page=1&per_page=20
```

**Response Example (200 OK):**
```json
{
  "success": true,
  "message": "Tasks retrieved successfully",
  "data": {
    "tasks": [
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
    ],
    "total": 45,
    "page": 1,
    "per_page": 20,
    "total_pages": 3,
    "has_next": true,
    "has_prev": false
  },
  "timestamp": "2024-01-17T10:30:00.123456"
}
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
{
  "success": true,
  "message": "Overdue tasks retrieved successfully",
  "data": [
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
  ],
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "Task retrieved successfully",
  "data": {
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
  },
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "Task updated successfully",
  "data": {
    "id": 1,
    "title": "Implement user authentication (Updated)",
    "status": "IN_PROGRESS",
    "priority": "CRITICAL",
    "actual_hours": 8.0,
    "completion_date": "2024-01-20T15:30:00Z",
    "labels": ["backend", "security", "urgent"],
    "updated_at": "2024-01-20T15:30:00Z"
  },
  "timestamp": "2024-01-20T15:30:00.123456"
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
  "success": true,
  "message": "Task deleted successfully",
  "data": null,
  "timestamp": "2024-01-20T15:30:00.123456"
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
  "success": true,
  "message": "Task assigned successfully",
  "data": {
    "id": 1,
    "title": "Implement user authentication",
    "assigned_to": {
      "id": 3,
      "name": "Bob Wilson",
      "email": "bob.wilson@example.com",
      "role": "SENIOR_DEVELOPER"
    },
    "comments": []
  },
  "timestamp": "2024-01-20T15:30:00.123456"
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
  "success": true,
  "message": "Comment added successfully",
  "data": {
    "id": 2,
    "text": "I've completed the login endpoint and started working on registration",
    "author": {
      "id": 2,
      "name": "Jane Smith"
    },
    "createdAt": "2024-01-17T11:20:00Z"
  },
  "timestamp": "2024-01-17T11:20:00.123456"
}
```

---

### Get User Time Logs
**Endpoint:** `GET /api/tasks/time-logs`  
**Description:** Get time logs for the current user  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `start_date` (string, optional) - Start date in YYYY-MM-DD format
- `end_date` (string, optional) - End date in YYYY-MM-DD format
- `limit` (integer, optional, default: 50) - Maximum number of records

**Response Example (200 OK):**
```json
{
  "success": true,
  "message": "Time logs retrieved successfully",
  "data": [
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
  },
  "timestamp": "2024-01-17T16:30:00.123456"
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
  "success": true,
  "message": "Task time logs retrieved successfully",
  "data": [
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
  ],
  "timestamp": "2024-01-17T16:30:00.123456"
}
```

---

### Get Daily Time Summary
**Endpoint:** `GET /api/tasks/time/daily-summary`  
**Description:** Get daily time summary for the current user  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `date` (string, optional) - Date in YYYY-MM-DD format (defaults to today)

**Response Example (200 OK):**
```json
{
  "success": true,
  "message": "Daily summary retrieved successfully",
  "data": {
    "date": "2024-01-17",
    "total_hours": 7.5,
    "user_id": 2
  },
  "timestamp": "2024-01-17T16:30:00.123456"
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
  "success": true,
  "message": "Project created successfully",
  "data": {
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
  },
  "timestamp": "2024-01-15T12:00:00.123456"
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
  "success": true,
  "message": "Projects retrieved successfully",
  "data": [
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
  ],
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "Project retrieved successfully",
  "data": {
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
  },
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "Project updated successfully",
  "data": {
    "id": 1,
    "name": "Updated Project Name",
    "description": "Updated project description",
    "status": "ACTIVE",
    "estimated_hours": 2200.0,
    "updated_at": "2024-01-17T14:30:00Z"
  },
  "timestamp": "2024-01-17T14:30:00.123456"
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
  "success": true,
  "message": "Project deleted successfully",
  "data": null,
  "timestamp": "2024-01-17T14:30:00.123456"
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
  "success": true,
  "message": "Recent projects retrieved successfully",
  "data": [
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
  ],
  "timestamp": "2024-01-17T14:30:00.123456"
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
  "success": true,
  "message": "Sprint created successfully",
  "data": {
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
    "created_at": "2024-01-15T12:00:00Z",
    "updated_at": "2024-01-15T12:00:00Z"
  },
  "timestamp": "2024-01-15T12:00:00.123456"
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
  "success": true,
  "message": "Sprint retrieved successfully",
  "data": {
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
  },
  "timestamp": "2024-02-01T09:00:00.123456"
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
  "success": true,
  "message": "Sprint updated successfully",
  "data": {
    "id": 1,
    "name": "Sprint 1 - Authentication & Security Module",
    "description": "Updated description with security focus",
    "goal": "Complete authentication system with enhanced security features",
    "capacity_hours": 90.0,
    "status": "ACTIVE",
    "updated_at": "2024-02-02T10:30:00Z"
  },
  "timestamp": "2024-02-02T10:30:00.123456"
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
  "success": true,
  "message": "Sprint deleted successfully",
  "data": null,
  "timestamp": "2024-02-02T10:30:00.123456"
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
  "success": true,
  "message": "Project sprints retrieved successfully",
  "data": [
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
  ],
  "timestamp": "2024-02-15T09:00:00.123456"
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
  "success": true,
  "message": "Sprint started successfully",
  "data": {
    "id": 1,
    "name": "Sprint 1 - Authentication Module",
    "status": "ACTIVE",
    "start_date": "2024-02-01T09:00:00Z",
    "updated_at": "2024-02-01T09:00:00Z"
  },
  "timestamp": "2024-02-01T09:00:00.123456"
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
  "success": true,
  "message": "Sprint completed successfully",
  "data": {
    "id": 1,
    "name": "Sprint 1 - Authentication Module",
    "status": "COMPLETED",
    "end_date": "2024-02-14T17:00:00Z",
    "velocity_points": 21,
    "updated_at": "2024-02-14T17:00:00Z"
  },
  "timestamp": "2024-02-14T17:00:00.123456"
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
  "success": true,
  "message": "Sprint burndown data retrieved successfully",
  "data": {
    "total_points": 21,
    "completed_points": 13,
    "remaining_points": 8,
    "completion_percentage": 61.9
  },
  "timestamp": "2024-02-10T10:00:00.123456"
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
  "success": true,
  "message": "Task added to sprint successfully",
  "data": {
    "id": 5,
    "title": "Implement password reset functionality",
    "sprint_id": 1,
    "story_points": 5,
    "status": "TODO"
  },
  "timestamp": "2024-02-10T10:00:00.123456"
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
  "success": true,
  "message": "Task removed from sprint successfully",
  "data": {
    "id": 5,
    "title": "Implement password reset functionality",
    "sprint_id": null,
    "status": "BACKLOG"
  },
  "timestamp": "2024-02-10T10:00:00.123456"
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
  "success": true,
  "message": "Comments retrieved successfully",
  "data": [
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
  ],
  "timestamp": "2024-01-17T11:20:00.123456"
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
  "success": true,
  "message": "Comment updated successfully",
  "data": {
    "id": 2,
    "comment": "Updated comment text with more details about the implementation",
    "updated_at": "2024-01-17T15:45:00Z"
  },
  "timestamp": "2024-01-17T15:45:00.123456"
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
  "success": true,
  "message": "Comment deleted successfully",
  "data": null,
  "timestamp": "2024-01-17T15:45:00.123456"
}
```

---

## Notifications

### Get Notification Summary
**Endpoint:** `GET /api/notifications/summary`  
**Description:** Get notification summary for dashboard  
**Authentication:** JWT Bearer Token required  

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response Example (200 OK):**
```json
{
  "success": true,
  "message": "Notification summary retrieved successfully",
  "data": {
    "total_notifications": 15,
    "unread_count": 3,
    "recent_notifications": [
      {
        "id": 1,
        "type": "TASK_ASSIGNED",
        "title": "New Task Assigned",
        "message": "You have been assigned to task: Implement user authentication",
        "read": false,
        "created_at": "2024-01-17T10:30:00Z"
      }
    ]
  },
  "timestamp": "2024-01-17T10:30:00.123456"
}
```

---

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
  "success": true,
  "message": "Unread notifications retrieved successfully",
  "data": [
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
  ],
  "timestamp": "2024-01-17T14:20:00.123456"
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
  "success": true,
  "message": "Notification marked as read",
  "data": {
    "id": 1,
    "read": true,
    "read_at": "2024-01-17T16:45:00Z"
  },
  "timestamp": "2024-01-17T16:45:00.123456"
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
  "success": true,
  "message": "All notifications marked as read",
  "data": {
    "updated_count": 5
  },
  "timestamp": "2024-01-17T16:45:00.123456"
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
  "success": true,
  "message": "Notification deleted successfully",
  "data": null,
  "timestamp": "2024-01-17T16:45:00.123456"
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
  "success": true,
  "message": "Task completion rate retrieved successfully",
  "data": {
    "time_period": "month",
    "total_tasks": 23,
    "completed_tasks": 20,
    "completion_rate": 0.87,
    "start_date": "2023-12-17T10:30:00Z",
    "end_date": "2024-01-17T10:30:00Z"
  },
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "User productivity data retrieved successfully",
  "data": {
    "total_tasks": 45,
    "completed_tasks": 40,
    "completion_rate": 0.89
  },
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "Task status distribution retrieved successfully",
  "data": {
    "BACKLOG": 25,
    "TODO": 18,
    "IN_PROGRESS": 32,
    "IN_REVIEW": 12,
    "TESTING": 8,
    "DONE": 55,
    "BLOCKED": 4,
    "CANCELLED": 2
  },
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "Task priority distribution retrieved successfully",
  "data": {
    "CRITICAL": 8,
    "HIGH": 35,
    "MEDIUM": 78,
    "LOW": 35
  },
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "All enums retrieved successfully",
  "data": {
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
  },
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "User roles retrieved successfully",
  "data": {
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
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "Task statuses retrieved successfully",
  "data": {
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
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "Task priorities retrieved successfully",
  "data": {
    "CRITICAL": "CRITICAL",
    "HIGH": "HIGH",
    "MEDIUM": "MEDIUM",
    "LOW": "LOW"
  },
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "Task types retrieved successfully",
  "data": {
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
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "Project statuses retrieved successfully",
  "data": {
    "PLANNING": "PLANNING",
    "ACTIVE": "ACTIVE",
    "ON_HOLD": "ON_HOLD",
    "COMPLETED": "COMPLETED",
    "CANCELLED": "CANCELLED"
  },
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "Sprint statuses retrieved successfully",
  "data": {
    "PLANNED": "PLANNED",
    "ACTIVE": "ACTIVE",
    "COMPLETED": "COMPLETED",
    "CANCELLED": "CANCELLED"
  },
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "Database connection healthy",
  "data": {
    "status": "healthy",
    "database": "connected"
  },
  "timestamp": "2024-01-17T10:30:00.123456"
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "success": false,
  "message": "Database connection failed",
  "data": {
    "status": "unhealthy",
    "error": "Connection timeout"
  },
  "timestamp": "2024-01-17T10:30:00.123456"
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
  "success": true,
  "message": "Service is healthy",
  "data": {
    "status": "healthy",
    "service": "task-management-api"
  },
  "timestamp": "2024-01-17T10:30:00.123456"
}
```

---

## Error Handling

### Standard Error Response Format
All error responses follow the standardized format:

```json
{
  "success": false,
  "message": "Error message describing what went wrong",
  "data": null,
  "timestamp": "2024-01-17T10:30:00.123456"
}
```

### Common Error Responses

**400 Bad Request - Missing Required Fields:**
```json
{
  "success": false,
  "message": "Missing required fields",
  "data": null,
  "timestamp": "2024-01-17T10:30:00.123456"
}
```

**401 Unauthorized:**
```json
{
  "success": false,
  "message": "Authentication required",
  "data": null,
  "timestamp": "2024-01-17T10:30:00.123456"
}
```

**403 Forbidden:**
```json
{
  "success": false,
  "message": "You don't have permission to perform this action",
  "data": null,
  "timestamp": "2024-01-17T10:30:00.123456"
}
```

**404 Not Found:**
```json
{
  "success": false,
  "message": "Task not found",
  "data": null,
  "timestamp": "2024-01-17T10:30:00.123456"
}
```

**422 Validation Error:**
```json
{
  "success": false,
  "message": "Validation failed",
  "data": null,
  "timestamp": "2024-01-17T10:30:00.123456"
}
```

**500 Internal Server Error:**
```json
{
  "success": false,
  "message": "Internal server error",
  "data": null,
  "timestamp": "2024-01-17T10:30:00.123456"
}
```

---

## Important Implementation Notes

### Response Format Changes
The API has been updated to use a standardized response format across all endpoints:

1. **All responses** now include:
   - `success`: Boolean indicating operation success
   - `message`: Descriptive message about the operation
   - `data`: The actual response payload (previously the root level data)
   - `timestamp`: ISO timestamp of the response

2. **Error handling** is consistent across all endpoints with the same format

3. **Frontend integration** will need to access response data via `response.data` instead of directly from the response root

### Key Differences from Original Documentation
- **Response Structure**: All data is now wrapped in the standardized format
- **Error Responses**: Consistent error format with `success: false`
- **Timestamps**: All responses include server timestamps
- **Pagination**: Pagination info is included in the `data` object for list endpoints
- **Message Field**: All responses include descriptive messages

### Migration Guide for Frontend
When updating frontend applications to use this API:

1. **Access data via `response.data`** instead of direct response access
2. **Check `response.success`** for operation status instead of HTTP status alone
3. **Use `response.message`** for user-friendly status messages
4. **Handle errors consistently** using the standardized error format

### Authentication
- All protected endpoints require `Authorization: Bearer <token>` header
- JWT tokens expire after 24 hours
- Include the token in all requests to protected endpoints

### Rate Limiting
- 1000 requests per hour per authenticated user
- 100 requests per hour per IP for public endpoints
- Rate limit headers included in responses

### CORS Support
- API supports cross-origin requests
- Appropriate CORS headers are included in responses
- Credentials are supported for authenticated requests

---

## Version Information
- **Current Version**: v1
- **Last Updated**: January 2024
- **Breaking Changes**: Response format standardization
- **Backward Compatibility**: Not maintained - all clients must update to new format

---

## Support
For technical support or questions about this API:
- GitHub Repository: [Task Management System](https://github.com/company/task-management)
- Documentation: Available at `/api/docs` when running locally
- Production API: `http://65.2.186.248:5000`

---

*This documentation reflects the current implementation with the standardized response format. All examples show the actual response structure returned by the API.*h 30m"
    }
  ],
  "timestamp": "2024-01-17T16:30:00.123456"
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
  "success": true,
  "message": "Time logged successfully",
  "data": {
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
    "hours_formatted": "3
```