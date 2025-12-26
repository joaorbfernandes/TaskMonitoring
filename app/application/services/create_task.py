from datetime import date
from app.domain.entities.task import Task
from app.domain.enums.task_priority import TaskPriority
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.logging.logger import get_logger


class CreateTaskUseCase:
    """
    Application use case responsible for creating a new Task.

    Orchestrates:
    - Input validation (light)
    - Domain Task creation
    - Persistence via repository
    """

    def __init__(self, task_repository: TaskRepository, logger=None):
        self._task_repository = task_repository
        self._logger = logger or get_logger(self.__class__.__name__)

    def execute(
        self,
        *,
        title: str,
        description: str,
        due_date: date,
        priority: TaskPriority,
    ) -> Task:
        self._logger.info(f"Creating task with title='{title}'")

        task = Task.create(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
        )

        self._task_repository.add(task)

        self._logger.info(f"Task created id={task.id}")

        return task