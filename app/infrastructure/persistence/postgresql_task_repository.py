import psycopg
from typing import Optional, List
from datetime import datetime

from app.domain.entities.task import Task
from app.domain.enums.task_status import TaskStatus
from app.domain.enums.task_priority import TaskPriority
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.logging.logger import get_logger


class PostgreSQLTaskRepository(TaskRepository):
    """
    PostgreSQL implementation of TaskRepository.

    Responsible ONLY for persistence.
    No business logic lives here.
    """

    def __init__(self, dsn: str, logger=None):
        self._dsn = dsn
        self._logger = logger or get_logger(self.__class__.__name__)

    def add(self, task: Task) -> None:
        self._logger.info(f"Persisting task id={task.id}")

        with psycopg.connect(self._dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO tasks (
                        id,
                        title,
                        description,
                        due_date,
                        status,
                        priority,
                        active,
                        created_at,
                        updated_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        task.id,
                        task.title,
                        task.description,
                        task.due_date,
                        task.status.value,
                        task.priority.value,
                        task.active,
                        task.created_at,
                        task.updated_at,
                    ),
                )

        self._logger.info(f"Task persisted id={task.id}")

    def get_by_id(self, task_id: int) -> Optional[Task]:
        self._logger.debug(f"Fetching task id={task_id}")

        with psycopg.connect(self._dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        title,
                        description,
                        due_date,
                        status,
                        priority,
                        active,
                        created_at,
                        updated_at
                    FROM tasks
                    WHERE id = %s
                    """,
                    (task_id,),
                )

                row = cur.fetchone()

                if row is None:
                    self._logger.debug(f"Task not found id={task_id}")
                    return None

                (
                    id_,
                    title,
                    description,
                    due_date,
                    status,
                    priority,
                    active,
                    created_at,
                    updated_at,
                ) = row

                return Task.rehydrate(
                    task_id=id_,
                    title=title,
                    description=description,
                    due_date=due_date,
                    status=TaskStatus(status),
                    priority=TaskPriority(priority),
                    active=active,
                    created_at=created_at,
                    updated_at=updated_at,
                )

    def list_all(self) -> List[Task]:
        self._logger.debug("Fetching all tasks")
        with psycopg.connect(self._dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        title,
                        description,
                        due_date,
                        status,
                        priority,
                        active,
                        created_at,
                        updated_at
                    FROM tasks
                    """
                )

                rows = cur.fetchall()

                return [
                    Task.rehydrate(
                        task_id=row[0],
                        title=row[1],
                        description=row[2],
                        due_date=row[3],
                        status=TaskStatus(row[4]),
                        priority=TaskPriority(row[5]),
                        active=row[6],
                        created_at=row[7],
                        updated_at=row[8],
                    )
                    for row in rows
                ]