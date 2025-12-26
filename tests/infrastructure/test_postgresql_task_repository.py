from datetime import date, datetime, UTC

import os

import psycopg
import pytest

from app.domain.entities.task import Task
from app.domain.enums.task_priority import TaskPriority
from app.infrastructure.persistence.postgresql_task_repository import PostgreSQLTaskRepository


@pytest.fixture(scope="session")
def postgres_dsn():
    if os.getenv("RUN_INFRA_TESTS") != "1":
        pytest.skip("Infrastructure tests disabled")

    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        pytest.fail("DATABASE_URL not set for infrastructure tests")

    return dsn

@pytest.fixture(autouse=True)
def clean_tasks_table(postgres_dsn: str):
    with psycopg.connect(postgres_dsn) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM task_core.tasks")
    yield

@pytest.mark.infrastructure
def test_add_and_get_task_roundtrip(postgres_dsn: str):
    repository = PostgreSQLTaskRepository(dsn=postgres_dsn)

    task = Task.create(
        title="Test Task",
        description="Persisted test task",
        due_date=date.today(),
        priority=TaskPriority.MEDIUM,
    )

    repository.add(task)

    loaded_task = repository.get_by_id(1)

    assert loaded_task is not None
    assert loaded_task.id is not None
    
    assert loaded_task.title == task.title
    assert loaded_task.description == task.description
    assert loaded_task.due_date == task.due_date
    assert loaded_task.status == task.status
    assert loaded_task.priority == task.priority
    assert loaded_task.active == task.active

    assert isinstance(loaded_task.created_at, datetime)
    assert isinstance(loaded_task.updated_at, datetime)

    assert loaded_task.created_at.utcoffset().total_seconds() == 0
    assert loaded_task.updated_at.utcoffset().total_seconds() == 0