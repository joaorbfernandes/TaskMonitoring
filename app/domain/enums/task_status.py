from enum import Enum


class TaskStatus(str, Enum):
    """
    Operational lifecycle state of a Task.

    This enum represents the current execution state of the task
    from a workflow perspective.

    Important:
    - This enum contains NO business logic.
    - State transition rules are validated in the application layer.
    """

    # Task exists but no work has started yet
    TODO = "TODO"

    # Task is currently being worked on
    IN_PROGRESS = "IN_PROGRESS"

    # Task cannot proceed due to an external dependency or blocker
    BLOCKED = "BLOCKED"

    # Final state: task is completed and should not return to other states
    DONE = "DONE"