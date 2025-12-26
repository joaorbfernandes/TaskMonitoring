from datetime import date, timedelta

from app.domain.entities.task import Task
from app.domain.enums.task_status import TaskStatus
from app.domain.enums.task_priority import TaskPriority
from app.domain.services.rules.overdue_rule import OverdueRule
from app.domain.services.rules.near_due_date_rule import NearDueDateRule
from app.domain.services.rules.blocked_rule import BlockedRule
from app.domain.services.task_flag_evaluator import TaskFlagEvaluator
from app.infrastructure.persistence.postgresql_task_repository import PostgreSQLTaskRepository
# from app.infrastructure.persistence.in_memory_task_repository import InMemoryTaskRepository
from app.application.services.evaluate_task_flag import EvaluateTaskFlagUseCase
from app.infrastructure.logging.logger import get_logger


def main() -> None:
    logger = get_logger("CLI")

    # -------------------------
    # Setup infrastructure
    # -------------------------
    # repository = InMemoryTaskRepository()

    POSTGRES_DSN = "postgresql://task_user:task_pass@127.0.0.1:5433/task_core"
    repository = PostgreSQLTaskRepository(dsn=POSTGRES_DSN)

    # -------------------------
    # Setup rules
    # -------------------------
    rules = [
        OverdueRule(),
        NearDueDateRule(warning_days=3),
        BlockedRule(),
    ]

    evaluator = TaskFlagEvaluator(rules=rules)

    use_case = EvaluateTaskFlagUseCase(
        task_repository=repository,
        evaluator=evaluator,
    )

    logger.info("========== SCENARIO 1: INACTIVE TASK ==========")

    task = Task.rehydrate(
        task_id=1,
        title="Archived task",
        description="Old task, no longer relevant",
        due_date=date.today() - timedelta(days=10),
        status=TaskStatus.BLOCKED,
        priority=TaskPriority.MEDIUM,
        active=False,
        created_at=date.today() - timedelta(days=30),
        updated_at=date.today(),
    )

    repository.add(task)

    logger.info("Task created with:")
    logger.info("- active = False")
    logger.info("- status = BLOCKED")
    logger.info("- due_date = in the past")

    evaluation = use_case.execute(task_id=1)

    logger.info("=== Evaluation result ===")
    logger.info(f"All flags: {evaluation.flags}")
    logger.info(f"Primary flag: {evaluation.primary_flag}")

    logger.info("Explanation:")
    logger.info("- Global pre-condition applied")
    logger.info("- Task is inactive")
    logger.info("- No rules evaluated")
    logger.info("- Result forced to NORMAL")

    logger.info("=== End of scenario ===")

    logger.info("========== SCENARIO 2: ACTIVE + NEAR DUE DATE ==========")

    task = Task.create(
        task_id=2,
        title="Prepare presentation",
        description="Slides for Monday meeting",
        due_date=date.today() + timedelta(days=2),
        priority=TaskPriority.MEDIUM,
    )

    repository.add(task)

    logger.info("Task created with:")
    logger.info("- active = True")
    logger.info("- status = TODO")
    logger.info("- due_date = today + 2 days")

    evaluation = use_case.execute(task_id=2)

    logger.info("=== Evaluation result ===")
    logger.info(f"All flags: {evaluation.flags}")
    logger.info(f"Primary flag: {evaluation.primary_flag}")

    logger.info("Explanation:")
    logger.info("- NearDueDateRule triggered")
    logger.info("- Flag = CRITICAL")
    logger.info("- No other rules applied")

    logger.info("=== End of scenario ===")

    logger.info("========== SCENARIO 3: BLOCKED + NEAR DUE DATE ==========")

    # -------------------------
    # Create task
    # -------------------------
    task = Task.rehydrate(
        task_id=3,
        title="Submit report",
        description="Quarterly financial report",
        due_date=date.today() + timedelta(days=2),
        status=TaskStatus.BLOCKED,
        priority=TaskPriority.MEDIUM,
        active=True,
        created_at=date.today() - timedelta(days=5),
        updated_at=date.today(),
    )

    repository.add(task)

    logger.info("Task created with:")
    logger.info("- status = BLOCKED")
    logger.info("- due_date = today + 2 days")
    logger.info("- active = True")

    # -------------------------
    # Evaluate
    # -------------------------
    evaluation = use_case.execute(task_id=3)

    logger.info("=== Evaluation result ===")
    logger.info(f"All flags: {evaluation.flags}")
    logger.info(f"Primary flag: {evaluation.primary_flag}")

    logger.info("Explanation:")
    logger.info("- BlockedRule → ATTENTION")
    logger.info("- NearDueDateRule → CRITICAL")
    logger.info("- CRITICAL dominates ATTENTION")

    logger.info("=== End of scenario ===")


if __name__ == "__main__":
    main()