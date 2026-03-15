from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Notification:
    id: str | None
    user_id: int
    subject: str
    message: str
    is_read: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    read_at: datetime | None = None

    def mark_as_read(self) -> None:
        self.is_read = True
        self.read_at = datetime.now(timezone.utc)
