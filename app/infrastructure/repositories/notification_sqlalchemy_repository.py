from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.notification import Notification
from app.domain.repositories.notification_repository import NotificationRepository
from app.infrastructure.models import NotificationModel


class SqlAlchemyNotificationRepository(NotificationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _to_domain(self, model: NotificationModel) -> Notification:
        return Notification(
            id=model.id,
            user_id=model.user_id,
            subject=model.subject,
            message=model.message,
            is_read=model.is_read,
            created_at=model.created_at,
            read_at=model.read_at,
        )

    async def create(self, notification: Notification) -> Notification:
        model = NotificationModel(
            user_id=notification.user_id,
            subject=notification.subject,
            message=notification.message,
            is_read=notification.is_read,
            created_at=notification.created_at,
            read_at=notification.read_at,
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def list_by_user_id(self, user_id: int) -> list[Notification]:
        stmt = (
            select(NotificationModel)
            .where(NotificationModel.user_id == user_id)
            .order_by(NotificationModel.created_at.desc())
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]

    async def get_by_id_and_user_id(self, notification_id: str, user_id: int) -> Notification | None:
        stmt = select(NotificationModel).where(
            NotificationModel.id == notification_id,
            NotificationModel.user_id == user_id,
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def update(self, notification: Notification) -> Notification:
        stmt = select(NotificationModel).where(NotificationModel.id == notification.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one()

        model.subject = notification.subject
        model.message = notification.message
        model.is_read = notification.is_read
        model.read_at = notification.read_at

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
