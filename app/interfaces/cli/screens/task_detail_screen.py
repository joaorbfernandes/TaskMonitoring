from app.domain.enums.task_status import TaskStatus
from app.interfaces.cli.repository_factory import get_task_repository


def run_task_detail_screen(task) -> None:
    while True:
        print("\n=== Tarefa ===")
        print(f"ID: {task.id}")
        print(f"Título: {task.title}")
        print(f"Prioridade: {task.priority.name}")
        print(f"Estado: {task.status.name}")
        print(f"Data limite: {task.due_date}")

        print("\n1. Marcar como DONE")
        print("2. Marcar como BLOCKED")
        print("0. Voltar")

        choice = input("\nID da tarefa (ENTER para voltar): ").strip()

        if not choice:
            return

        repository = get_task_repository()

        if choice == "1":
            task.update_status(TaskStatus.DONE)
            repository.update(task)
            print("Tarefa concluída")

        elif choice == "2":
            task.update_status(TaskStatus.BLOCKED)
            repository.update(task)
            print("Tarefa bloqueada")

        elif choice == "0":
            break

        else:
            print("Opção inválida")