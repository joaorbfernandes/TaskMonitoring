from enum import Enum


class TaskPriority(str, Enum):
    """
    Human-defined priority of a Task.

    Represents the importance assigned by a user.
    It expresses intent, not system evaluation.

    Important:
    - Priority does NOT change automatically.
    - Priority is NOT recalculated by the system.
    """

    # Low urgency, minimal impact if delayed
    LOW = "LOW"

    # Normal priority for most tasks
    MEDIUM = "MEDIUM"

    # High importance task that requires attention
    HIGH = "HIGH"