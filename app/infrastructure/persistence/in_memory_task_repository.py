from typing import Dict, List, Optional

from app.domain.entities.task import Task
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.logging.logger import get_logger




class InMemoryTaskRepository(TaskRepository):
    """
    Simple in-memory implementation of TaskRepository.

    Used for tests, demos and local execution.
    """

    def __init__(self, logger=None):
        self._tasks: Dict[int, Task] = {}
        self._logger = logger or get_logger(self.__class__.__name__)

        self._logger.info("InMemoryTaskRepository initialized")

    def add(self, task: Task) -> None:
        self._tasks[task.id] = task
        self._logger.debug(f"Task added to memory: id={task.id}")

    def get_by_id(self, task_id: int) -> Optional[Task]:
        task = self._tasks.get(task_id)

        if task is None:
            self._logger.debug(f"Task not found in memory: id={task_id}")
        else:
            self._logger.debug(f"Task retrieved from memory: id={task_id}")

        return task

    def list_all(self) -> List[Task]:
        self._logger.debug(f"Listing all tasks. count={len(self._tasks)}")
        return list(self._tasks.values())