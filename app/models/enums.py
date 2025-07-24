# app/models/enums.py
from enum import Enum

class UserRole(Enum):
    ADMIN = "ADMIN"
    PROJECT_MANAGER = "PROJECT_MANAGER"
    TEAM_LEAD = "TEAM_LEAD"
    SENIOR_DEVELOPER = "SENIOR_DEVELOPER"
    DEVELOPER = "DEVELOPER"
    QA_ENGINEER = "QA_ENGINEER"
    DEVOPS_ENGINEER = "DEVOPS_ENGINEER"
    UI_UX_DESIGNER = "UI_UX_DESIGNER"
    BUSINESS_ANALYST = "BUSINESS_ANALYST"
    PRODUCT_OWNER = "PRODUCT_OWNER"
    SCRUM_MASTER = "SCRUM_MASTER"

class TaskStatus(Enum):
    BACKLOG = "BACKLOG"
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW"
    TESTING = "TESTING"
    BLOCKED = "BLOCKED"
    DONE = "DONE"
    CANCELLED = "CANCELLED"
    DEPLOYED = "DEPLOYED"

class TaskPriority(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class TaskType(Enum):
    FEATURE = "FEATURE"
    BUG = "BUG"
    ENHANCEMENT = "ENHANCEMENT"
    REFACTOR = "REFACTOR"
    DOCUMENTATION = "DOCUMENTATION"
    TESTING = "TESTING"
    DEPLOYMENT = "DEPLOYMENT"
    RESEARCH = "RESEARCH"
    MAINTENANCE = "MAINTENANCE"
    SECURITY = "SECURITY"

class ProjectStatus(Enum):
    PLANNING = "PLANNING"
    ACTIVE = "ACTIVE"
    ON_HOLD = "ON_HOLD"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class SprintStatus(Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class NotificationType(Enum):
    TASK_ASSIGNED = "TASK_ASSIGNED"
    TASK_UPDATED = "TASK_UPDATED"
    TASK_COMPLETED = "TASK_COMPLETED"
    TASK_OVERDUE = "TASK_OVERDUE"
    COMMENT_ADDED = "COMMENT_ADDED"
    PROJECT_UPDATED = "PROJECT_UPDATED"
    SPRINT_STARTED = "SPRINT_STARTED"
    SPRINT_COMPLETED = "SPRINT_COMPLETED"
    MENTION = "MENTION"

class EstimationUnit(Enum):
    HOURS = "HOURS"
    DAYS = "DAYS"
    STORY_POINTS = "STORY_POINTS"

# Utility methods for serialization
def enum_to_list(enum_class):
    """Returns a list of enum values."""
    return [e.value for e in enum_class]

def enum_to_dict(enum_class):
    """Returns a dictionary of enum names and values."""
    return {e.name: e.value for e in enum_class}

def get_all_enums():
    """Returns all enums for API documentation."""
    return {
        'UserRole': enum_to_dict(UserRole),
        'TaskStatus': enum_to_dict(TaskStatus),
        'TaskPriority': enum_to_dict(TaskPriority),
        'TaskType': enum_to_dict(TaskType),
        'ProjectStatus': enum_to_dict(ProjectStatus),
        'SprintStatus': enum_to_dict(SprintStatus),
        'NotificationType': enum_to_dict(NotificationType),
        'EstimationUnit': enum_to_dict(EstimationUnit)
    }