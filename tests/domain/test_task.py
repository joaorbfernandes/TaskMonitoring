import pytest
from datetime import date, timedelta, datetime, UTC

from app.domain.entities.task import Task
from app.domain.enums.task_status import TaskStatus
from app.domain.enums.task_priority import TaskPriority

def test_task_cannot_be_created_without_title():
    with pytest.raises(ValueError):
        Task.create(
            task_id=1,
            title="",
            description="No title",
            due_date=date.today() + timedelta(days=1),
            priority=TaskPriority.MEDIUM,
        )

def test_create_rejects_due_date_in_the_past():
    with pytest.raises(ValueError):
        Task.create(
            task_id=1,
            title="Invalid due date",
            description="Past date",
            due_date=date.today() - timedelta(days=1),
            priority=TaskPriority.MEDIUM,
        )

def test_rehydrate_accepts_past_due_date():
    task = Task.rehydrate(
        task_id=1,
        title="Old task",
        description="Historical data",
        due_date=date.today() - timedelta(days=10),
        status=TaskStatus.TODO,
        priority=TaskPriority.MEDIUM,
        active=True,
        created_at=datetime.now(UTC) - timedelta(days=20),
        updated_at=datetime.now(UTC),
    )

    assert task.due_date < date.today()

def test_create_sets_initial_state_correctly():
    task = Task.create(
        task_id=1,
        title="New task",
        description="Fresh task",
        due_date=date.today() + timedelta(days=3),
        priority=TaskPriority.HIGH,
    )

    assert task.status == TaskStatus.TODO
    assert task.active is True

def test_mark_inactive_sets_task_as_inactive():
    task = Task.create(
        task_id=1,
        title="Task to deactivate",
        description="Deactivate me",
        due_date=date.today() + timedelta(days=5),
        priority=TaskPriority.MEDIUM,
    )

    task.mark_inactive()

    assert task.active is False