from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.task import Task


class TaskRepository(ABC):

    @abstractmethod
    def add(self, task: Task) -> None:
        pass

    @abstractmethod
    def update(self, task: Task) -> None:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def list_all(self) -> List[Task]:
        pass