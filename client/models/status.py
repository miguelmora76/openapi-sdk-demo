from enum import StrEnum


class Status(StrEnum):
    APPROVED = "approved"
    DENIED = "denied"
    SUBMITTED = "submitted"

    def __str__(self) -> str:
        return str(self.value)
