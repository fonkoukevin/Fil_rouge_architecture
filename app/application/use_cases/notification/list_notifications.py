from app.domain.repositories.notification_repository import NotificationRepository


class ListNotificationsUseCase:
    def __init__(self, notification_repository: NotificationRepository) -> None:
        self.notification_repository = notification_repository

    async def execute(self, user_id: int):
        return await self.notification_repository.list_by_user_id(user_id)
