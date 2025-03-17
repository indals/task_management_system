#app/models/enums.py
from enum import Enum

class UserRole(Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"

class TaskStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class TaskPriority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

# Utility methods for serialization
def enum_to_list(enum_class):
    """Returns a list of enum values."""
    return [e.value for e in enum_class]

def enum_to_dict(enum_class):
    """Returns a dictionary of enum names and values."""
    return {e.name: e.value for e in enum_class}
