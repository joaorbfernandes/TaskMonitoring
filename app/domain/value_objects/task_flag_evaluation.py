from typing import List
from app.domain.value_objects.task_flag import TaskFlag


class TaskFlagEvaluation:
    """
    Represents the result of evaluating a Task.

    - Holds all triggered flags
    - Determines the primary (most severe) flag
    """

    def __init__(self, flags: List[TaskFlag]):
        # Store all triggered flags (can be empty)
        self._flags = list(flags)

        # Determine primary flag based on severity
        self._primary_flag = TaskFlag.most_severe(self._flags)

    @property
    def flags(self) -> List[TaskFlag]:
        """All flags triggered during evaluation."""
        return list(self._flags)

    @property
    def primary_flag(self) -> TaskFlag:
        """Most severe flag."""
        return self._primary_flag