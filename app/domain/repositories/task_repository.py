from typing import Protocol, List, Optional
from app.domain.entities.task import Task


class TaskRepository(Protocol):
    """
    Domain repository interface for Task aggregate.

    Defines how Tasks are retrieved and persisted,
    without knowing implementation details.
    """

    def add(self, task: Task) -> None:
        """
        Persist a new task.

        The repository decides how persistence is handled.
        """
        ...

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its identifier.

        Returns None if the task does not exist.
        """
        ...

    def list_all(self) -> List[Task]:
        """
        Retrieve all tasks.
        """
        ...