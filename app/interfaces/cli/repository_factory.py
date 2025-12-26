import os

from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.persistence.in_memory_task_repository import InMemoryTaskRepository
from app.infrastructure.persistence.postgresql_task_repository import PostgreSQLTaskRepository


def get_task_repository() -> TaskRepository:
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return PostgreSQLTaskRepository(dsn=database_url)

    return InMemoryTaskRepository()