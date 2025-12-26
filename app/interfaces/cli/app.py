from app.interfaces.cli.screens.create_task_screen import run_create_task_screen
from app.interfaces.cli.screens.list_tasks_screen import run_list_tasks_screen


def run():
    while True:
        print("\n=== Task Manager ===")
        print("1. Criar tarefa")
        print("2. Listar tarefas")
        print("0. Sair")

        choice = input("Escolhe uma opção: ").strip()

        if choice == "1":
            run_create_task_screen()
        elif choice == "2":
            run_list_tasks_screen()
        elif choice == "0":
            print("Até logo 👋")
            break
        else:
            print("Opção inválida")