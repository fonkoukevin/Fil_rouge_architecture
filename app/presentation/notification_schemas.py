from datetime import datetime
from pydantic import BaseModel


class NotificationResponse(BaseModel):
    id: str
    user_id: int
    subject: str
    message: str
    is_read: bool
    created_at: datetime
    read_at: datetime | None
