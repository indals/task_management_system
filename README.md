
task_management_system/
├── venv/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── enums.py
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── task_comment.py
│   │   └── notification.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── task_service.py
│   │   ├── notification_service.py
│   │   └── analytics_service.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── task_routes.py
│   │   ├── notification_routes.py
│   │   └── analytics_routes.py
│   └── utils/
│       └── __init__.py
├── config.py
├── run.py
├── .env
└── requirements.txt






flowchart TD
    subgraph Client["Client Layer"]
        A[Angular Frontend]
        B[Material UI Components]
    end

    subgraph API["API Gateway Layer"]
        C[Flask REST API Server]
        D[WebSocket Server]
    end

    subgraph Services["Service Layer"]
        E[Authentication Service]
        F[Task Management Service]
        G[Analytics Service]
        H[Notification Service]
    end

    subgraph Data["Data Layer"]
        I[(PostgreSQL Database)]
    end

    A <--> C
    A <--> D
    B --- A
    C --> E
    C --> F
    C --> G
    C --> H
    E --> I
    F --> I
    G --> I
    H --> I















erDiagram
    Users {
        int id PK
        string name
        string email
        string password_hash
        enum role
        datetime created_at
        datetime updated_at
    }
    
    Tasks {
        int id PK
        string title
        string description
        enum status
        enum priority
        int assigned_to FK
        int created_by FK
        datetime due_date
        datetime created_at
        datetime updated_at
    }
    
    TaskComments {
        int id PK
        int task_id FK
        int user_id FK
        string comment
        datetime created_at
    }
    
    Notifications {
        int id PK
        int user_id FK
        int task_id FK
        string message
        boolean read
        datetime created_at
    }

    Users ||--o{ Tasks : "creates"
    Users ||--o{ Tasks : "assigned_to"
    Tasks ||--o{ TaskComments : "has"
    Users ||--o{ TaskComments : "creates"
    Users ||--o{ Notifications : "receives"
    Tasks ||--o{ Notifications : "generates"



















sequenceDiagram
    actor User
    participant Frontend as Angular Frontend
    participant API as Flask API
    participant Auth as Auth Service
    participant TaskSvc as Task Service
    participant DB as Database
    participant WS as WebSocket Server

    User->>Frontend: Create New Task
    Frontend->>API: POST /api/tasks
    API->>Auth: Validate JWT
    Auth-->>API: Token Valid
    API->>TaskSvc: Create Task
    TaskSvc->>DB: Insert Task
    DB-->>TaskSvc: Task Created
    TaskSvc->>WS: Broadcast Task Creation
    WS-->>Frontend: Real-time Update
    TaskSvc-->>API: Task Details
    API-->>Frontend: Success Response
    Frontend-->>User: Task Created Successfully




























flask shell
from app import db
db.create_all()
Step 3: Verify in PostgreSQL
Reconnect to PostgreSQL:

sh
Copy
Edit
psql "postgresql://postgres:VGbtoCXHgBeOUzXmFxIULvZfZbwXqnDM@hopper.proxy.rlwy.net:20422/railway"
Check if tables exist:

sql
Copy
Edit
\dt