from datetime import date, timedelta

from app.domain.entities.task import Task
from app.domain.enums.task_status import TaskStatus
from app.domain.enums.task_priority import TaskPriority
from app.domain.services.rules.overdue_rule import OverdueRule
from app.domain.services.rules.near_due_date_rule import NearDueDateRule
from app.domain.services.rules.blocked_rule import BlockedRule
from app.domain.services.task_flag_evaluator import TaskFlagEvaluator
from app.domain.value_objects.task_flag import TaskFlag
from app.infrastructure.persistence.in_memory_task_repository import InMemoryTaskRepository
from app.application.services.evaluate_task_flag import EvaluateTaskFlagUseCase

import pytest

@pytest.fixture
def repository():
    return InMemoryTaskRepository()

@pytest.fixture
def evaluator():
    return TaskFlagEvaluator(
        rules=[
            OverdueRule(),
            NearDueDateRule(warning_days=3),
            BlockedRule(),
        ]
    )

# -------------------------
# Tests
# -------------------------


def test_evaluate_task_flags_use_case_inactive_task_returns_normal(repository,evaluator):

    task = Task.rehydrate(
        task_id=1,
        title="Inactive Task",
        description="Should not be evaluated",
        due_date=date.today() - timedelta(days=10),  
        status=TaskStatus.BLOCKED,                   
        priority=TaskPriority.MEDIUM,
        active=False,                                
        created_at=date.today() - timedelta(days=20),
        updated_at=date.today(),
    )

    repository.add(task)

    use_case = EvaluateTaskFlagUseCase(repository,evaluator)

    result = use_case.execute(task_id=1)

    assert result.flags == [TaskFlag.NORMAL]
    assert result.primary_flag == TaskFlag.NORMAL

def test_evaluate_task_flags_use_case_inactive_task_returns_normal(repository,evaluator):
    task = Task.rehydrate(
        task_id=1,
        title="Inactive Task",
        description="Should not be evaluated",
        due_date=date.today() - timedelta(days=10),
        status=TaskStatus.BLOCKED,
        priority=TaskPriority.MEDIUM,
        active=False,
        created_at=date.today() - timedelta(days=20),
        updated_at=date.today(),
    )

    repository.add(task)

    use_case = EvaluateTaskFlagUseCase(repository,evaluator)

    result = use_case.execute(task_id=1)

    assert result.flags == [TaskFlag.NORMAL]
    assert result.primary_flag == TaskFlag.NORMAL

def test_evaluate_task_flags_use_case_near_due_date_returns_critical(repository,evaluator):

    task = Task.rehydrate(
        task_id=1,
        title="Near Due Task",
        description="Almost overdue",
        due_date=date.today() + timedelta(days=2),
        status=TaskStatus.TODO,
        priority=TaskPriority.MEDIUM,
        active=True,
        created_at=date.today() - timedelta(days=5),
        updated_at=date.today(),
    )

    repository.add(task)

    use_case = EvaluateTaskFlagUseCase(repository,evaluator)

    result = use_case.execute(task_id=1)

    assert result.flags == [TaskFlag.CRITICAL]
    assert result.primary_flag == TaskFlag.CRITICAL

def test_evaluate_task_flags_use_case_overdue_returns_overdue(repository,evaluator):

    task = Task.rehydrate(
        task_id=1,
        title="Overdue Task",
        description="Already late",
        due_date=date.today() - timedelta(days=1),
        status=TaskStatus.TODO,
        priority=TaskPriority.MEDIUM,
        active=True,
        created_at=date.today() - timedelta(days=10),
        updated_at=date.today(),
    )

    repository.add(task)

    use_case = EvaluateTaskFlagUseCase(repository,evaluator)

    result = use_case.execute(task_id=1)

    assert result.flags == [TaskFlag.OVERDUE]
    assert result.primary_flag == TaskFlag.OVERDUE

def test_evaluate_task_flags_use_case_primary_critical(repository,evaluator):

    task = Task.rehydrate(
        task_id=1,
        title="Near Due Task",
        description="Almost overdue",
        due_date=date.today() + timedelta(days=2),
        status=TaskStatus.BLOCKED,
        priority=TaskPriority.MEDIUM,
        active=True,
        created_at=date.today() - timedelta(days=5),
        updated_at=date.today(),
    )

    repository.add(task)

    use_case = EvaluateTaskFlagUseCase(repository,evaluator)

    result = use_case.execute(task_id=1)

    assert TaskFlag.CRITICAL in result.flags
    assert TaskFlag.ATTENTION in result.flags
    assert result.primary_flag == TaskFlag.CRITICAL

def test_evaluate_task_flags_use_case_primary_overdue(repository,evaluator):

    task = Task.rehydrate(
        task_id=1,
        title="Test Task",
        description="Test Description",
        due_date=date.today() - timedelta(days=1),
        status=TaskStatus.BLOCKED,
        priority=TaskPriority.MEDIUM,
        active=True,
        created_at=date.today() - timedelta(days=10),
        updated_at=date.today(),
    )

    repository.add(task)

    use_case = EvaluateTaskFlagUseCase(repository,evaluator)

    result = use_case.execute(task_id=1)

    assert TaskFlag.OVERDUE in result.flags
    assert TaskFlag.ATTENTION in result.flags
    assert result.primary_flag == TaskFlag.OVERDUE

'''
(TODO) CHECK IF THIS CAN REALLY HAPPEN OTHERWISE NOT NECESSARY -- DELETE
'''
def test_evaluate_task_flags_use_case_raises_error_when_task_does_not_exist(repository,evaluator): 

    use_case = EvaluateTaskFlagUseCase(repository,evaluator)

    # Act + Assert
    with pytest.raises(ValueError, match="Task with id 999 not found"):
        use_case.execute(task_id=999)