from datetime import date
from app.domain.entities.task import Task
from app.domain.enums.task_status import TaskStatus
from app.domain.services.rules.base_rule import BaseTaskFlagRule
from app.domain.value_objects.task_flag import TaskFlag


class OverdueRule(BaseTaskFlagRule):
    """
    Rule: Task is overdue.

    Evaluates whether a task has passed its due date
    and is not yet completed.
    """

    def evaluate(self, task: Task) -> TaskFlag | None:
        # Completed tasks are never overdue
        if task.status == TaskStatus.DONE:
            return None

        # If current date is past the due date, task is overdue
        if date.today() > task.due_date:
            return TaskFlag.OVERDUE

        return None
    