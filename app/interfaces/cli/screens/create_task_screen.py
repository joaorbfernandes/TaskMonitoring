from datetime import date

from app.application.services.create_task import CreateTaskUseCase
from app.application.services.evaluate_task_flag import EvaluateTaskFlagUseCase
from app.domain.enums.task_priority import TaskPriority
from app.domain.services.rules.overdue_rule import OverdueRule
from app.domain.services.rules.near_due_date_rule import NearDueDateRule
from app.domain.services.rules.blocked_rule import BlockedRule
from app.domain.services.task_flag_evaluator import TaskFlagEvaluator
from app.interfaces.cli.repository_factory import get_task_repository


def run_create_task_screen():
    print("\n=== Criar Tarefa ===")

    title = input("Título: ").strip()
    if not title:
        print("Título é obrigatório")
        return

    due_date_raw = input("Data limite (YYYY-MM-DD): ").strip()
    try:
        due_date = date.fromisoformat(due_date_raw)
    except ValueError:
        print("Data inválida")
        return

    priority_raw = input("Prioridade [LOW/MEDIUM/HIGH]: ").strip().upper()
    if priority_raw not in ("LOW", "MEDIUM", "HIGH"):
        print("Prioridade inválida")
        return

    repository = get_task_repository()

    create_use_case = CreateTaskUseCase(
        task_repository=repository
    )

    task = create_use_case.execute(
        title=title,
        description="",
        due_date=due_date,
        priority=TaskPriority[priority_raw],
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

    print("\n✔ Tarefa criada com sucesso")
    print(f"ID: {task.id}")
    print(f"Título: {task.title}")
    print(f"Prioridade: {task.priority.name}")
    print(f"Estado automático: {evaluation.primary_flag.value}")

    input("\n[ENTER] para voltar ao menu")