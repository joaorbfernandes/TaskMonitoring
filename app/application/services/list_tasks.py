class ListTasksUseCase:
    def __init__(self, task_repository):
        self._repository = task_repository

    def execute(self):
        return self._repository.list_all()