from app.domain.repositories.task_repository import TaskRepository
from app.domain.services.task_flag_evaluator import TaskFlagEvaluator
from app.domain.value_objects.task_flag_evaluation import TaskFlagEvaluation
from app.infrastructure.logging.logger import get_logger


class EvaluateTaskFlagUseCase:
    """
    Application use case responsible for evaluating task flags.

    Orchestrates:
    - Task retrieval
    - Domain flag evaluation
    """

    def __init__(
        self,
        task_repository: TaskRepository,
        evaluator: TaskFlagEvaluator,
        logger=None,
    ):
        self._task_repository = task_repository
        self._evaluator = evaluator
        self._logger = logger or get_logger(self.__class__.__name__)

    def execute(self, task_id: int) -> TaskFlagEvaluation:
        self._logger.info(f"Starting task flag evaluation for task_id={task_id}")

        task = self._task_repository.get_by_id(task_id)

        if task is None:
            self._logger.warning(f"Task not found: task_id={task_id}")
            raise ValueError(f"Task with id {task_id} not found")

        evaluation = self._evaluator.evaluate(task)

        self._logger.info(
            f"Finished task flag evaluation for task_id={task_id} | "
            f"primary_flag={evaluation.primary_flag} | "
            f"all_flags={evaluation.flags}"
        )

        return evaluation