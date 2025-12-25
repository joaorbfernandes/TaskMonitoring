from enum import Enum


class TaskFlag(str, Enum):
    """
    Automatic system evaluation of a Task.

    This value object represents the severity level assigned by the system
    after applying monitoring rules.

    Characteristics:
    - Not persisted by default
    - Fully recalculable
    - Does NOT belong to the Task entity
    - Result of interpretation, not human decision
    """

    # String values
    # - Stable for APIs and persistence if ever needed
    NORMAL = "NORMAL"
    ATTENTION = "ATTENTION"
    CRITICAL = "CRITICAL"
    OVERDUE = "OVERDUE"

    @property
    def severity(self) -> int:
        """
        Numeric severity used for comparison.
        Higher value means higher severity.
        """
        return {
            TaskFlag.NORMAL: 0,
            TaskFlag.ATTENTION: 1,
            TaskFlag.CRITICAL: 2,
            TaskFlag.OVERDUE: 3,
        }[self]

    @classmethod
    def most_severe(cls, flags: list["TaskFlag"]) -> "TaskFlag":
        """
        Returns the most severe flag from a list of flags.
        Defaults to NORMAL if the list is empty.
        """
        if not flags:
            return cls.NORMAL

        return max(flags, key=lambda flag: flag.severity)
