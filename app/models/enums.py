# app/models/enums.py
from enum import Enum

# Import logging and caching utilities
from app.utils.logger import get_logger, log_db_query
from app.utils.cache_utils import cache, cached_per_user, CacheKeys

# Initialize logger for this module
logger = get_logger('enums')

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
    TASK_STATUS_CHANGED = "TASK_STATUS_CHANGED"
    TASK_COMPLETED = "TASK_COMPLETED"
    TASK_OVERDUE = "TASK_OVERDUE"
    TASK_DUE_SOON = "TASK_DUE_SOON"
    TASK_COMMENT = "TASK_COMMENT"
    COMMENT_ADDED = "COMMENT_ADDED"
    PROJECT_UPDATED = "PROJECT_UPDATED"
    SPRINT_STARTED = "SPRINT_STARTED"
    SPRINT_COMPLETED = "SPRINT_COMPLETED"
    MENTION = "MENTION"

class EstimationUnit(Enum):
    HOURS = "HOURS"
    DAYS = "DAYS"
    STORY_POINTS = "STORY_POINTS"

# Utility methods for serialization with logging
def enum_to_list(enum_class):
    """Returns a list of enum values with logging."""
    logger.debug(f"Converting {enum_class.__name__} to list")
    values = [e.value for e in enum_class]
    logger.debug(f"Generated {len(values)} values for {enum_class.__name__}")
    return values

def enum_to_dict(enum_class):
    """Returns a dictionary of enum names and values with logging."""
    logger.debug(f"Converting {enum_class.__name__} to dictionary")
    result = {e.name: e.value for e in enum_class}
    logger.debug(f"Generated {len(result)} key-value pairs for {enum_class.__name__}")
    return result

def format_label(value):
    """Format enum value to readable label with logging."""
    logger.debug(f"Formatting label for value: {value}")
    formatted = value.replace('_', ' ').title()
    logger.debug(f"Formatted '{value}' to '{formatted}'")
    return formatted

# Enhanced enum configurations
TASK_TYPE_CONFIG = {
    'FEATURE': {'label': 'Feature', 'icon': 'fa-star', 'color': '#28a745', 'default_estimation_unit': 'STORY_POINTS', 'requires_approval': False, 'workflow_impact': 'high'},
    'BUG': {'label': 'Bug', 'icon': 'fa-bug', 'color': '#dc3545', 'default_estimation_unit': 'HOURS', 'requires_approval': False, 'workflow_impact': 'critical'},
    'ENHANCEMENT': {'label': 'Enhancement', 'icon': 'fa-arrow-up', 'color': '#17a2b8', 'default_estimation_unit': 'STORY_POINTS', 'requires_approval': False, 'workflow_impact': 'medium'},
    'REFACTOR': {'label': 'Refactor', 'icon': 'fa-code', 'color': '#6f42c1', 'default_estimation_unit': 'HOURS', 'requires_approval': True, 'workflow_impact': 'medium'},
    'TESTING': {'label': 'Testing', 'icon': 'fa-check', 'color': '#fd7e14', 'default_estimation_unit': 'HOURS', 'requires_approval': False, 'workflow_impact': 'high'},
    'DOCUMENTATION': {'label': 'Documentation', 'icon': 'fa-file-text', 'color': '#6c757d', 'default_estimation_unit': 'HOURS', 'requires_approval': False, 'workflow_impact': 'low'},
    'MAINTENANCE': {'label': 'Maintenance', 'icon': 'fa-wrench', 'color': '#20c997', 'default_estimation_unit': 'HOURS', 'requires_approval': False, 'workflow_impact': 'medium'},
    'SECURITY': {'label': 'Security', 'icon': 'fa-shield', 'color': '#e83e8c', 'default_estimation_unit': 'STORY_POINTS', 'requires_approval': True, 'workflow_impact': 'critical'},
    'DEPLOYMENT': {'label': 'Deployment', 'icon': 'fa-rocket', 'color': '#007bff', 'default_estimation_unit': 'HOURS', 'requires_approval': True, 'workflow_impact': 'high'},
    'RESEARCH': {'label': 'Research', 'icon': 'fa-search', 'color': '#ffc107', 'default_estimation_unit': 'STORY_POINTS', 'requires_approval': False, 'workflow_impact': 'low'}
}

TASK_PRIORITY_CONFIG = {
    'CRITICAL': {'label': 'Critical', 'icon': 'fa-exclamation-triangle', 'color': '#dc3545', 'severity_level': 4, 'escalation_hours': 4, 'notification_frequency': 'immediate'},
    'HIGH': {'label': 'High', 'icon': 'fa-arrow-up', 'color': '#fd7e14', 'severity_level': 3, 'escalation_hours': 24, 'notification_frequency': 'hourly'},
    'MEDIUM': {'label': 'Medium', 'icon': 'fa-minus', 'color': '#ffc107', 'severity_level': 2, 'escalation_hours': 72, 'notification_frequency': 'daily'},
    'LOW': {'label': 'Low', 'icon': 'fa-arrow-down', 'color': '#28a745', 'severity_level': 1, 'escalation_hours': 168, 'notification_frequency': 'weekly'}
}

TASK_STATUS_CONFIG = {
    'BACKLOG': {'label': 'Backlog', 'icon': 'fa-inbox', 'color': '#6c757d', 'is_completed': False, 'is_active': False, 'next_statuses': ['TODO'], 'workflow_stage': 'planning'},
    'TODO': {'label': 'To Do', 'icon': 'fa-circle-o', 'color': '#17a2b8', 'is_completed': False, 'is_active': False, 'next_statuses': ['IN_PROGRESS'], 'workflow_stage': 'ready'},
    'IN_PROGRESS': {'label': 'In Progress', 'icon': 'fa-play', 'color': '#ffc107', 'is_completed': False, 'is_active': True, 'next_statuses': ['IN_REVIEW', 'BLOCKED'], 'workflow_stage': 'development'},
    'IN_REVIEW': {'label': 'In Review', 'icon': 'fa-eye', 'color': '#fd7e14', 'is_completed': False, 'is_active': True, 'next_statuses': ['TESTING', 'IN_PROGRESS'], 'workflow_stage': 'review'},
    'TESTING': {'label': 'Testing', 'icon': 'fa-flask', 'color': '#e83e8c', 'is_completed': False, 'is_active': True, 'next_statuses': ['DONE', 'IN_PROGRESS'], 'workflow_stage': 'qa'},
    'DONE': {'label': 'Done', 'icon': 'fa-check', 'color': '#28a745', 'is_completed': True, 'is_active': False, 'next_statuses': ['DEPLOYED'], 'workflow_stage': 'complete'},
    'DEPLOYED': {'label': 'Deployed', 'icon': 'fa-rocket', 'color': '#20c997', 'is_completed': True, 'is_active': False, 'next_statuses': [], 'workflow_stage': 'deployed'},
    'BLOCKED': {'label': 'Blocked', 'icon': 'fa-ban', 'color': '#dc3545', 'is_completed': False, 'is_active': False, 'next_statuses': ['IN_PROGRESS'], 'workflow_stage': 'blocked'},
    'CANCELLED': {'label': 'Cancelled', 'icon': 'fa-times', 'color': '#6c757d', 'is_completed': True, 'is_active': False, 'next_statuses': [], 'workflow_stage': 'cancelled'}
}

USER_ROLE_CONFIG = {
    'ADMIN': {'label': 'Administrator', 'icon': 'fa-crown', 'color': '#dc3545', 'hierarchy_level': 10, 'permissions': ['all'], 'can_manage_users': True, 'can_delete_projects': True},
    'PROJECT_MANAGER': {'label': 'Project Manager', 'icon': 'fa-users', 'color': '#007bff', 'hierarchy_level': 9, 'permissions': ['project_management'], 'can_manage_users': True, 'can_delete_projects': True},
    'TEAM_LEAD': {'label': 'Team Lead', 'icon': 'fa-user-tie', 'color': '#6f42c1', 'hierarchy_level': 8, 'permissions': ['team_management'], 'can_manage_users': False, 'can_delete_projects': False},
    'SENIOR_DEVELOPER': {'label': 'Senior Developer', 'icon': 'fa-code', 'color': '#28a745', 'hierarchy_level': 7, 'permissions': ['development', 'review'], 'can_manage_users': False, 'can_delete_projects': False},
    'DEVELOPER': {'label': 'Developer', 'icon': 'fa-laptop-code', 'color': '#17a2b8', 'hierarchy_level': 6, 'permissions': ['development'], 'can_manage_users': False, 'can_delete_projects': False},
    'QA_ENGINEER': {'label': 'QA Engineer', 'icon': 'fa-check-double', 'color': '#fd7e14', 'hierarchy_level': 6, 'permissions': ['testing'], 'can_manage_users': False, 'can_delete_projects': False},
    'DEVOPS_ENGINEER': {'label': 'DevOps Engineer', 'icon': 'fa-server', 'color': '#20c997', 'hierarchy_level': 7, 'permissions': ['deployment', 'infrastructure'], 'can_manage_users': False, 'can_delete_projects': False},
    'UI_UX_DESIGNER': {'label': 'UI/UX Designer', 'icon': 'fa-paint-brush', 'color': '#e83e8c', 'hierarchy_level': 6, 'permissions': ['design'], 'can_manage_users': False, 'can_delete_projects': False},
    'BUSINESS_ANALYST': {'label': 'Business Analyst', 'icon': 'fa-chart-line', 'color': '#ffc107', 'hierarchy_level': 7, 'permissions': ['analysis'], 'can_manage_users': False, 'can_delete_projects': False},
    'PRODUCT_OWNER': {'label': 'Product Owner', 'icon': 'fa-bullseye', 'color': '#6f42c1', 'hierarchy_level': 8, 'permissions': ['product_management'], 'can_manage_users': False, 'can_delete_projects': False},
    'SCRUM_MASTER': {'label': 'Scrum Master', 'icon': 'fa-clipboard-list', 'color': '#fd7e14', 'hierarchy_level': 7, 'permissions': ['scrum_management'], 'can_manage_users': False, 'can_delete_projects': False}
}

PROJECT_STATUS_CONFIG = {
    'PLANNING': {'label': 'Planning', 'icon': 'fa-clipboard', 'color': '#ffc107', 'is_active': False, 'allows_new_tasks': True, 'requires_approval_to_change': False},
    'ACTIVE': {'label': 'Active', 'icon': 'fa-play', 'color': '#28a745', 'is_active': True, 'allows_new_tasks': True, 'requires_approval_to_change': False},
    'ON_HOLD': {'label': 'On Hold', 'icon': 'fa-pause', 'color': '#fd7e14', 'is_active': False, 'allows_new_tasks': False, 'requires_approval_to_change': True},
    'COMPLETED': {'label': 'Completed', 'icon': 'fa-check', 'color': '#20c997', 'is_active': False, 'allows_new_tasks': False, 'requires_approval_to_change': True},
    'CANCELLED': {'label': 'Cancelled', 'icon': 'fa-times', 'color': '#dc3545', 'is_active': False, 'allows_new_tasks': False, 'requires_approval_to_change': True}
}

SPRINT_STATUS_CONFIG = {
    'PLANNED': {'label': 'Planned', 'icon': 'fa-calendar', 'color': '#6c757d', 'is_active': False, 'allows_task_changes': True, 'can_start': True},
    'ACTIVE': {'label': 'Active', 'icon': 'fa-play', 'color': '#28a745', 'is_active': True, 'allows_task_changes': True, 'can_start': False},
    'COMPLETED': {'label': 'Completed', 'icon': 'fa-check', 'color': '#20c997', 'is_active': False, 'allows_task_changes': False, 'can_start': False},
    'CANCELLED': {'label': 'Cancelled', 'icon': 'fa-times', 'color': '#dc3545', 'is_active': False, 'allows_task_changes': False, 'can_start': False}
}

ESTIMATION_UNIT_CONFIG = {
    'STORY_POINTS': {'label': 'Story Points', 'icon': 'fa-star', 'color': '#007bff', 'conversion_factor': 1.0, 'default_value': 5, 'fibonacci_scale': True},
    'HOURS': {'label': 'Hours', 'icon': 'fa-clock', 'color': '#28a745', 'conversion_factor': 8.0, 'default_value': 4, 'fibonacci_scale': False},
    'DAYS': {'label': 'Days', 'icon': 'fa-calendar-day', 'color': '#ffc107', 'conversion_factor': 64.0, 'default_value': 1, 'fibonacci_scale': False}
}

NOTIFICATION_TYPE_CONFIG = {
    'TASK_ASSIGNED': {'label': 'Task Assigned', 'icon': 'fa-user-plus', 'color': '#007bff', 'priority': 'medium', 'sound_alert': True},
    'TASK_UPDATED': {'label': 'Task Updated', 'icon': 'fa-edit', 'color': '#17a2b8', 'priority': 'low', 'sound_alert': False},
    'TASK_STATUS_CHANGED': {'label': 'Task Status Changed', 'icon': 'fa-exchange-alt', 'color': '#ffc107', 'priority': 'medium', 'sound_alert': False},
    'TASK_COMPLETED': {'label': 'Task Completed', 'icon': 'fa-check-circle', 'color': '#28a745', 'priority': 'medium', 'sound_alert': True},
    'TASK_OVERDUE': {'label': 'Task Overdue', 'icon': 'fa-exclamation-triangle', 'color': '#dc3545', 'priority': 'high', 'sound_alert': True},
    'TASK_DUE_SOON': {'label': 'Task Due Soon', 'icon': 'fa-clock', 'color': '#fd7e14', 'priority': 'medium', 'sound_alert': False},
    'TASK_COMMENT': {'label': 'New Comment', 'icon': 'fa-comment', 'color': '#6f42c1', 'priority': 'low', 'sound_alert': False},
    'COMMENT_ADDED': {'label': 'Comment Added', 'icon': 'fa-comment-alt', 'color': '#6f42c1', 'priority': 'low', 'sound_alert': False},
    'PROJECT_UPDATED': {'label': 'Project Updated', 'icon': 'fa-project-diagram', 'color': '#20c997', 'priority': 'medium', 'sound_alert': False},
    'SPRINT_STARTED': {'label': 'Sprint Started', 'icon': 'fa-play-circle', 'color': '#28a745', 'priority': 'high', 'sound_alert': True},
    'SPRINT_COMPLETED': {'label': 'Sprint Completed', 'icon': 'fa-flag-checkered', 'color': '#20c997', 'priority': 'high', 'sound_alert': True},
    'MENTION': {'label': 'Mentioned', 'icon': 'fa-at', 'color': '#e83e8c', 'priority': 'high', 'sound_alert': True}
}

def transform_enum_to_rich_objects(enum_class, config_dict, default_config):
    """Transform enum to rich objects with metadata and logging."""
    logger.debug(f"Transforming {enum_class.__name__} to rich objects")
    result = []
    
    for item in enum_class:
        config = config_dict.get(item.value, {
            'label': format_label(item.value),
            **default_config
        })
        
        enum_obj = {'value': item.value}
        enum_obj.update(config)
        result.append(enum_obj)
    
    logger.debug(f"Generated {len(result)} rich objects for {enum_class.__name__}")
    return result

@cache.cached(timeout=3600, key_prefix='all_enums_rich')
def get_all_enums():
    """Returns all enums with rich metadata for frontend with comprehensive logging."""
    logger.info("Generating comprehensive enums data for frontend")
    
    try:
        enums_data = {
            'user_roles': transform_enum_to_rich_objects(
                UserRole, 
                USER_ROLE_CONFIG, 
                {'icon': 'fa-user', 'color': '#6c757d', 'hierarchy_level': 5, 'permissions': [], 'can_manage_users': False, 'can_delete_projects': False}
            ),
            'task_statuses': transform_enum_to_rich_objects(
                TaskStatus, 
                TASK_STATUS_CONFIG, 
                {'icon': 'fa-circle', 'color': '#6c757d', 'is_completed': False, 'is_active': False, 'next_statuses': [], 'workflow_stage': 'unknown'}
            ),
            'task_priorities': transform_enum_to_rich_objects(
                TaskPriority, 
                TASK_PRIORITY_CONFIG, 
                {'icon': 'fa-minus', 'color': '#6c757d', 'severity_level': 2, 'escalation_hours': 72, 'notification_frequency': 'daily'}
            ),
            'task_types': transform_enum_to_rich_objects(
                TaskType, 
                TASK_TYPE_CONFIG, 
                {'icon': 'fa-tasks', 'color': '#6c757d', 'default_estimation_unit': 'STORY_POINTS', 'requires_approval': False, 'workflow_impact': 'medium'}
            ),
            'project_statuses': transform_enum_to_rich_objects(
                ProjectStatus, 
                PROJECT_STATUS_CONFIG, 
                {'icon': 'fa-circle', 'color': '#6c757d', 'is_active': False, 'allows_new_tasks': False, 'requires_approval_to_change': False}
            ),
            'sprint_statuses': transform_enum_to_rich_objects(
                SprintStatus, 
                SPRINT_STATUS_CONFIG, 
                {'icon': 'fa-circle', 'color': '#6c757d', 'is_active': False, 'allows_task_changes': False, 'can_start': False}
            ),
            'estimation_units': transform_enum_to_rich_objects(
                EstimationUnit, 
                ESTIMATION_UNIT_CONFIG, 
                {'icon': 'fa-ruler', 'color': '#6c757d', 'conversion_factor': 1.0, 'default_value': 1, 'fibonacci_scale': False}
            ),
            'notification_types': transform_enum_to_rich_objects(
                NotificationType,
                NOTIFICATION_TYPE_CONFIG,
                {'icon': 'fa-bell', 'color': '#6c757d', 'priority': 'low', 'sound_alert': False}
            )
        }
        
        logger.info(f"Successfully generated enums data with {len(enums_data)} categories")
        return enums_data
        
    except Exception as e:
        logger.error(f"Failed to generate enums data: {str(e)}")
        raise

@cache.cached(timeout=1800, key_prefix='enum_workflows')
def get_workflow_configurations():
    """Get workflow configurations for different enum types with caching."""
    logger.debug("Generating workflow configurations")
    
    workflows = {
        'task_status_workflow': {
            'stages': ['planning', 'ready', 'development', 'review', 'qa', 'complete', 'deployed'],
            'transitions': get_status_transitions(),
            'completion_stages': ['complete', 'deployed', 'cancelled']
        },
        'priority_escalation': {
            'rules': get_priority_escalation_rules(),
            'notification_schedules': get_notification_schedules()
        },
        'approval_workflows': {
            'task_types_requiring_approval': get_task_types_requiring_approval(),
            'status_changes_requiring_approval': get_status_changes_requiring_approval()
        }
    }
    
    logger.debug(f"Generated {len(workflows)} workflow configurations")
    return workflows

@cache.cached(timeout=900, key_prefix='enum_permissions')
def get_role_permissions_matrix():
    """Get detailed role permissions matrix with caching."""
    logger.debug("Generating role permissions matrix")
    
    permissions_matrix = {}
    for role in UserRole:
        config = USER_ROLE_CONFIG.get(role.value, {})
        permissions_matrix[role.value] = {
            'hierarchy_level': config.get('hierarchy_level', 5),
            'permissions': config.get('permissions', []),
            'can_manage_users': config.get('can_manage_users', False),
            'can_delete_projects': config.get('can_delete_projects', False),
            'can_approve_tasks': config.get('hierarchy_level', 5) >= 7,
            'can_change_project_status': config.get('hierarchy_level', 5) >= 8,
            'can_manage_sprints': 'scrum_management' in config.get('permissions', []) or config.get('hierarchy_level', 5) >= 8
        }
    
    logger.debug(f"Generated permissions for {len(permissions_matrix)} roles")
    return permissions_matrix

def get_status_transitions():
    """Get valid status transitions with logging."""
    logger.debug("Calculating status transitions")
    transitions = {}
    
    for status in TaskStatus:
        config = TASK_STATUS_CONFIG.get(status.value, {})
        transitions[status.value] = config.get('next_statuses', [])
    
    logger.debug(f"Generated transitions for {len(transitions)} statuses")
    return transitions

def get_priority_escalation_rules():
    """Get priority escalation rules with logging."""
    logger.debug("Generating priority escalation rules")
    rules = {}
    
    for priority in TaskPriority:
        config = TASK_PRIORITY_CONFIG.get(priority.value, {})
        rules[priority.value] = {
            'escalation_hours': config.get('escalation_hours', 72),
            'severity_level': config.get('severity_level', 2),
            'notification_frequency': config.get('notification_frequency', 'daily')
        }
    
    logger.debug(f"Generated escalation rules for {len(rules)} priorities")
    return rules

def get_notification_schedules():
    """Get notification schedules by priority with logging."""
    logger.debug("Generating notification schedules")
    schedules = {}
    
    for priority in TaskPriority:
        config = TASK_PRIORITY_CONFIG.get(priority.value, {})
        frequency = config.get('notification_frequency', 'daily')
        
        schedules[priority.value] = {
            'frequency': frequency,
            'intervals': {
                'immediate': [0],  # minutes
                'hourly': [0, 60, 120, 240],  # every hour, then 2h, then 4h
                'daily': [0, 1440, 2880],  # daily for 3 days
                'weekly': [0, 10080]  # weekly
            }.get(frequency, [0, 1440])
        }
    
    logger.debug(f"Generated schedules for {len(schedules)} priorities")
    return schedules

def get_task_types_requiring_approval():
    """Get task types that require approval with logging."""
    logger.debug("Identifying task types requiring approval")
    
    requiring_approval = []
    for task_type in TaskType:
        config = TASK_TYPE_CONFIG.get(task_type.value, {})
        if config.get('requires_approval', False):
            requiring_approval.append(task_type.value)
    
    logger.debug(f"Found {len(requiring_approval)} task types requiring approval")
    return requiring_approval

def get_status_changes_requiring_approval():
    """Get status changes that require approval with logging."""
    logger.debug("Identifying status changes requiring approval")
    
    # Generally, moving to final states requires approval
    requiring_approval = {
        'to_completed': ['DONE', 'DEPLOYED', 'CANCELLED'],
        'from_completed': ['DONE', 'DEPLOYED'],
        'priority_changes': ['CRITICAL']
    }
    
    logger.debug("Generated status change approval requirements")
    return requiring_approval

@cache.cached(timeout=600, key_prefix='enum_validation')
def get_validation_rules():
    """Get validation rules for enum values with caching."""
    logger.debug("Generating validation rules for enums")
    
    validation_rules = {
        'task_status': {
            'required_fields_by_status': {
                'IN_PROGRESS': ['assigned_to_id'],
                'IN_REVIEW': ['assigned_to_id', 'estimated_hours'],
                'TESTING': ['assigned_to_id'],
                'DONE': ['completed_by_id', 'actual_hours']
            },
            'forbidden_transitions': [
                ('BACKLOG', 'DONE'),
                ('TODO', 'DEPLOYED'),
                ('CANCELLED', 'IN_PROGRESS')
            ]
        },
        'user_role': {
            'hierarchy_restrictions': get_hierarchy_restrictions(),
            'permission_requirements': get_permission_requirements()
        }
    }
    
    logger.debug("Generated comprehensive validation rules")
    return validation_rules

def get_hierarchy_restrictions():
    """Get role hierarchy restrictions with logging."""
    logger.debug("Generating role hierarchy restrictions")
    
    restrictions = {}
    for role in UserRole:
        config = USER_ROLE_CONFIG.get(role.value, {})
        level = config.get('hierarchy_level', 5)
        
        restrictions[role.value] = {
            'can_assign_to_levels': list(range(1, level + 1)),
            'can_be_managed_by_levels': list(range(level, 11)),
            'can_manage_levels': list(range(1, level))
        }
    
    logger.debug(f"Generated hierarchy restrictions for {len(restrictions)} roles")
    return restrictions

def get_permission_requirements():
    """Get permission requirements with logging."""
    logger.debug("Generating permission requirements")
    
    requirements = {
        'create_project': ['hierarchy_level >= 8'],
        'delete_project': ['can_delete_projects = true'],
        'manage_users': ['can_manage_users = true'],
        'assign_critical_tasks': ['hierarchy_level >= 7'],
        'approve_deployments': ['deployment in permissions OR hierarchy_level >= 9'],
        'manage_sprints': ['scrum_management in permissions OR hierarchy_level >= 8']
    }
    
    logger.debug(f"Generated {len(requirements)} permission requirements")
    return requirements

# def validate_enum_value(enum_class, value, context=None):
#     """Validate enum value with logging and context."""
#     logger.debug(f"Validating {enum_class.__name__} value: {value}")
    
#     try:
#         enum_value =