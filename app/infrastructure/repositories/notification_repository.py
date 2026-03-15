from abc import ABC, abstractmethod

from app.domain.entities.notification import Notification


class NotificationRepository(ABC):
    @abstractmethod
    async def create(self, notification: Notification) -> Notification:
        pass

    @abstractmethod
    async def list_by_user_id(self, user_id: int) -> list[Notification]:
        pass

    @abstractmethod
    async def get_by_id_and_user_id(self, notification_id: str, user_id: int) -> Notification | None:
        pass

    @abstractmethod
    async def update(self, notification: Notification) -> Notification:
        pass
