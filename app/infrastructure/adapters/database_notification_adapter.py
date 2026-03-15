from app.domain.entities.notification import Notification
from app.domain.ports.notification_port import NotificationPort
from app.domain.repositories.notification_repository import NotificationRepository


class DatabaseNotificationAdapter(NotificationPort):
    def __init__(self, notification_repository: NotificationRepository) -> None:
        self.notification_repository = notification_repository

    async def send(self, user_id: int, subject: str, message: str) -> None:
        notification = Notification(
            id=None,
            user_id=user_id,
            subject=subject,
            message=message,
            is_read=False,
        )
        await self.notification_repository.create(notification)
