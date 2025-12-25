from app.domain.entities.task import Task
from app.domain.enums.task_status import TaskStatus
from app.domain.services.rules.base_rule import BaseTaskFlagRule
from app.domain.value_objects.task_flag import TaskFlag


class NearDueDateRule(BaseTaskFlagRule):
    """
    Rule: Task is approaching its due date.

    Evaluates whether a task that is not completedis close to its due date, based on a configurable
    warning window (in days).
    """

    def __init__(self, warning_days: int):
        if warning_days <= 0:
            raise ValueError("warning_days must be greater than zero")

        self._warning_days = warning_days

    def evaluate(self, task: Task) -> TaskFlag | None:
        # Completed tasks are ignored
        if task.status == TaskStatus.DONE:
            return None

        # days_until_due is a derived attribute from Task
        days_until_due = task.days_until_due

        # Only future deadlines inside the warning window
        if 0 < days_until_due <= self._warning_days:
            return TaskFlag.CRITICAL

        return None