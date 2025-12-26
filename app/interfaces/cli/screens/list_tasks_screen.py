from app.interfaces.cli.repository_factory import get_task_repository
from app.interfaces.cli.screens.task_detail_screen import run_task_detail_screen


def run_list_tasks_screen() -> None:
    print("\n=== Tarefas ===\n")

    repository = get_task_repository()
    tasks = repository.list_all()

    if not tasks:
        print("Nenhuma tarefa encontrada.")
        input("\n[ENTER] para voltar ao menu")
        return

    for task in tasks:
        print(f"[{task.id}] {task.title} | {task.priority.name} | {task.status.name}")

    choice = input("\nID da tarefa (ENTER para voltar): ").strip()

    if not choice:
        return

    if not choice.isdigit():
        print("ID inválido")
        input("[ENTER] para continuar")
        return

    task = repository.get_by_id(int(choice))

    if not task:
        print("Tarefa não encontrada")
        input("[ENTER] para continuar")
        return

    run_task_detail_screen(task)