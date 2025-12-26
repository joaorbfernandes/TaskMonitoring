from datetime import datetime, date, UTC
from app.domain.enums.task_status import TaskStatus
from app.domain.enums.task_priority import TaskPriority


class Task:
    """
    Aggregate Root: Task

    Represents a unit of work with human decisions and operational state.
    """

    def __init__(
        self,
        task_id: int | None,
        title: str,
        description: str | None,
        due_date: date,
        status: TaskStatus,
        priority: TaskPriority,
        active: bool = True,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        # --- invariants / validation ---
        if not title:
            raise ValueError("Task title cannot be empty")

        '''(TODO) [DELETE]
        if due_date < date.today():
            raise ValueError("Due date cannot be in the past")'''

        # --- persisted attributes ---
        self._id = task_id
        self._title = title
        self._description = description
        self._due_date = due_date
        self._status = status
        self._priority = priority
        self._active = active

        now = datetime.now(UTC)

        self._created_at = created_at or now
        self._updated_at = updated_at or now

    # -------------------------
    # Factory methods
    # -------------------------

    @classmethod
    def create(
        cls,
        title: str,
        description: str | None,
        due_date: date,
        priority: TaskPriority,
    ) -> "Task":
        if due_date < date.today():
            raise ValueError("Due date cannot be in the past")

        return cls(
            task_id=None,
            title=title,
            description=description,
            due_date=due_date,
            status=TaskStatus.TODO,
            priority=priority,
            active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

    @classmethod
    def rehydrate(
        cls,
        *,
        task_id: int,
        title: str,
        description: str,
        due_date: date,
        status: TaskStatus,
        priority: TaskPriority,
        active: bool,
        created_at: datetime,
        updated_at: datetime,
    ) -> "Task":
        return cls(
            task_id=task_id,
            title=title,
            description=description,
            due_date=due_date,
            status=status,
            priority=priority,
            active=active,
            created_at=created_at,
            updated_at=updated_at,
        )
    
    # -------------------------
    # Read-only properties
    # -------------------------

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def due_date(self) -> date:
        return self._due_date

    @property
    def status(self) -> TaskStatus:
        return self._status

    @property
    def priority(self) -> TaskPriority:
        return self._priority

    @property
    def active(self) -> bool:
        return self._active

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    # -------------------------
    # Derived attributes
    # -------------------------
    
    @property
    def days_until_due(self) -> int:
        delta = self._due_date - datetime.now(UTC).date()
        return delta.days

    # -------------------------
    # Domain behaviour (explicit, controlled)
    # -------------------------

    def mark_inactive(self) -> None:
        """
        Archives or deactivates the task.
        """
        if not self._active:
            return

        self._active = False
        self._touch()

    def update_status(self, new_status: TaskStatus) -> None:
        """
        Updates the operational status.
        Validation of transitions happens in the application layer.
        """
        self._status = new_status
        self._touch()

    def update_priority(self, new_priority: TaskPriority) -> None:
        """
        Updates human-defined priority.
        """
        self._priority = new_priority
        self._touch()

    # -------------------------
    # Internal helpers
    # -------------------------

    def _touch(self) -> None:
        self._updated_at = datetime.now(UTC)