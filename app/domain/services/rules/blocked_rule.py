from app.domain.entities.task import Task
from app.domain.enums.task_status import TaskStatus
from app.domain.services.rules.base_rule import BaseTaskFlagRule
from app.domain.value_objects.task_flag import TaskFlag


class BlockedRule(BaseTaskFlagRule):
    """
    Rule: Task is blocked.

    This rule evaluates the operational state of a task.
    A blocked task indicates an external dependency or impediment
    that prevents progress and therefore requires human attention.

    This rule is:
    - Orthogonal to time-based rules (e.g. overdue, near due date)
    - Independent from other rules
    - Non-mutating (does not change task state)
    """

    def evaluate(self, task: Task) -> TaskFlag | None:
        """
        Evaluates whether the task is currently blocked.

        Returns:
        - TaskFlag.ATTENTION if the task is blocked
        - None otherwise
        """

        # A blocked task always requires attention,
        # regardless of due date or priority
        if task.status == TaskStatus.BLOCKED:
            return TaskFlag.ATTENTION

        # No operational issue detected
        return None