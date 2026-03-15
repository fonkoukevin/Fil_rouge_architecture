from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.notification.list_notifications import ListNotificationsUseCase
from app.application.use_cases.notification.mark_notification_as_read import (
    MarkNotificationAsReadUseCase,
    NotificationNotFoundError,
)
from app.infrastructure.database import get_db
from app.infrastructure.repositories.notification_sqlalchemy_repository import (
    SqlAlchemyNotificationRepository,
)
from app.presentation.auth_dependencies import get_current_user_id
from app.presentation.notification_schemas import NotificationResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=list[NotificationResponse])
async def list_notifications(
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    repository = SqlAlchemyNotificationRepository(session)
    use_case = ListNotificationsUseCase(repository)
    return await use_case.execute(current_user_id)


@router.post("/{notification_id}/lu", response_model=NotificationResponse)
async def mark_as_read(
    notification_id: str,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    repository = SqlAlchemyNotificationRepository(session)
    use_case = MarkNotificationAsReadUseCase(repository)

    try:
        notification = await use_case.execute(notification_id, current_user_id)
        await session.commit()
        return notification
    except NotificationNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
