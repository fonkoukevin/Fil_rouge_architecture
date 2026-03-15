from abc import ABC, abstractmethod


class NotificationPort(ABC):
    @abstractmethod
    async def send(self, user_id: int, subject: str, message: str) -> None:
        pass
