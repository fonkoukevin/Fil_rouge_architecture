from app.domain.repositories.notification_repository import NotificationRepository


class NotificationNotFoundError(Exception):
    pass


class MarkNotificationAsReadUseCase:
    def __init__(self, notification_repository: NotificationRepository) -> None:
        self.notification_repository = notification_repository

    async def execute(self, notification_id: str, user_id: int):
        notification = await self.notification_repository.get_by_id_and_user_id(
            notification_id=notification_id,
            user_id=user_id,
        )
        if notification is None:
            raise NotificationNotFoundError("Notification introuvable.")

        notification.mark_as_read()
        return await self.notification_repository.update(notification)
