from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.publication.publish_manuscript import (
    PublishManuscriptUseCase,
    PublicationError,
    ManuscriptNotFoundError,
)

from app.infrastructure.database import get_db
from app.infrastructure.repositories.manuscript_sqlalchemy_repository import (
    SqlAlchemyManuscriptRepository,
)
from app.infrastructure.repositories.book_sqlalchemy_repository import (
    SqlAlchemyBookRepository,
)

from app.infrastructure.repositories.notification_sqlalchemy_repository import (
    SqlAlchemyNotificationRepository,
)
from app.infrastructure.adapters.database_notification_adapter import (
    DatabaseNotificationAdapter,
)

from app.presentation.auth_dependencies import get_current_user_id


router = APIRouter(prefix="/publications", tags=["Publication"])


@router.post("")
async def publish_manuscript(
    manuscript_id: str,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):

    manuscript_repo = SqlAlchemyManuscriptRepository(session)
    book_repo = SqlAlchemyBookRepository(session)

    notification_repo = SqlAlchemyNotificationRepository(session)
    notification_adapter = DatabaseNotificationAdapter(notification_repo)

    use_case = PublishManuscriptUseCase(
        manuscript_repo,
        book_repo,
        notification_adapter,
    )

    try:
        book = await use_case.execute(
            manuscript_id=manuscript_id,
            current_user_id=current_user_id,
        )

        await session.commit()
        return book

    except ManuscriptNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc))

    except PublicationError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(exc))
