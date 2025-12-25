from abc import ABC, abstractmethod
from app.domain.entities.task import Task
from app.domain.value_objects.task_flag import TaskFlag


class BaseTaskFlagRule(ABC):
    """
    Base contract for all TaskFlag rules.

    Rules:
    - Are independent
    - Do not alter task state
    - Do not know other rules
    """

    @abstractmethod
    def evaluate(self, task: Task) -> TaskFlag | None:
        """
        Evaluates the rule condition.

        Returns:
        - TaskFlag if the rule applies
        - None if it does not apply
        """
        raise NotImplementedError