from datetime import date

from app.application.services.create_task import CreateTaskUseCase
from app.application.services.evaluate_task_flag import EvaluateTaskFlagUseCase
from app.domain.enums.task_priority import TaskPriority
from app.domain.services.rules.overdue_rule import OverdueRule
from app.domain.services.rules.near_due_date_rule import NearDueDateRule
from app.domain.services.rules.blocked_rule import BlockedRule
from app.domain.services.task_flag_evaluator import TaskFlagEvaluator
from app.interfaces.cli.repository_factory import get_task_repository


def register_create_task_command(subparsers):
    parser = subparsers.add_parser(
        "create",
        help="Create a new task",
    )

    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--due-date", required=True)
    parser.add_argument(
        "--priority",
        choices=["LOW", "MEDIUM", "HIGH"],
        default="MEDIUM",
    )

    parser.set_defaults(func=_handle_create_task)

def _handle_create_task(args):
    repository = get_task_repository()

    create_use_case = CreateTaskUseCase(
        task_repository=repository
    )

    task = create_use_case.execute(
        title=args.title,
        description=args.description,
        due_date=date.fromisoformat(args.due_date),
        priority=TaskPriority[args.priority],
    )

    evaluator = TaskFlagEvaluator(
        rules=[
            OverdueRule(),
            NearDueDateRule(warning_days=3),
            BlockedRule(),
        ]
    )

    evaluate_use_case = EvaluateTaskFlagUseCase(
        task_repository=repository,
        evaluator=evaluator,
    )

    evaluation = evaluate_use_case.execute(task.id)

    print("\nTask criada:")
    print(f"- ID: {task.id}")
    print(f"- Title: {task.title}")
    print(f"- Due date: {task.due_date}")
    print(f"- Priority: {task.priority.name}")

    print("\nAvaliação automática:")
    print(f"- Flags: {[f.value for f in evaluation.flags]}")
    print(f"- Primary flag: {evaluation.primary_flag.value}")