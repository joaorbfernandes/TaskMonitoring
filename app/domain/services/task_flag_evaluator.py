from typing import Iterable, List
from app.domain.entities.task import Task
from app.domain.services.rules.base_rule import BaseTaskFlagRule
from app.domain.value_objects.task_flag import TaskFlag
from app.domain.value_objects.task_flag_evaluation import TaskFlagEvaluation
from app.infrastructure.logging.logger import get_logger


class TaskFlagEvaluator:
    """
    Domain Service responsible for evaluating a Task and producing a TaskFlagEvaluation.
    """

    def __init__(self, rules: Iterable[BaseTaskFlagRule], logger=None):
        self._rules = list(rules)
        self._logger = logger or get_logger(self.__class__.__name__)

    def evaluate(self, task: Task) -> TaskFlagEvaluation:
        task_ref = getattr(task, "id", "<no-id>")
        self._logger.info(f"Evaluating task {task_ref}")

        # Global pre-condition
        if not task.active:
            self._logger.info(f"Task {task.id} is inactive. Returning NORMAL evaluation.")
            return TaskFlagEvaluation(flags=[TaskFlag.NORMAL])

        triggered_flags: List[TaskFlag] = []

        for rule in self._rules:
            result = rule.evaluate(task)
            if result is not None:
                self._logger.debug(f"Rule {rule.__class__.__name__} triggered: {result}")
                triggered_flags.append(result)

        evaluation = TaskFlagEvaluation(triggered_flags)

        self._logger.info(f"Task {task.id} evaluation result: primary={evaluation.primary_flag}, all_flags={evaluation.flags}"
        )

        return evaluation