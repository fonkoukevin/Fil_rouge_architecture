from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.editorial.submit_manuscript import (
    SubmitManuscriptUseCase,
    ManuscriptAlreadySubmittedError,
    ManuscriptNotFoundError,
)
from app.application.use_cases.editorial.start_review import (
    StartReviewUseCase,
    EditorialDossierNotFoundError,
)
from app.application.use_cases.editorial.request_changes import RequestChangesUseCase
from app.application.use_cases.editorial.accept_dossier import AcceptDossierUseCase
from app.application.use_cases.editorial.reject_dossier import RejectDossierUseCase

from app.infrastructure.database import get_db
from app.infrastructure.repositories.manuscript_sqlalchemy_repository import (
    SqlAlchemyManuscriptRepository,
)
from app.infrastructure.repositories.editorial_dossier_sqlalchemy_repository import (
    SqlAlchemyEditorialDossierRepository,
)

from app.infrastructure.repositories.notification_sqlalchemy_repository import (
    SqlAlchemyNotificationRepository,
)
from app.infrastructure.adapters.database_notification_adapter import (
    DatabaseNotificationAdapter,
)

from app.presentation.auth_dependencies import get_current_user_id


router = APIRouter(prefix="/editorial", tags=["Editorial"])


# --------------------------------------------------
# Soumettre un manuscrit
# --------------------------------------------------

@router.post("/manuscrits/{manuscript_id}/soumettre")
async def submit_manuscript(
    manuscript_id: str,
    note: str | None = None,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):

    manuscript_repo = SqlAlchemyManuscriptRepository(session)
    dossier_repo = SqlAlchemyEditorialDossierRepository(session)

    notification_repo = SqlAlchemyNotificationRepository(session)
    notification_adapter = DatabaseNotificationAdapter(notification_repo)

    use_case = SubmitManuscriptUseCase(
        manuscript_repo,
        dossier_repo,
        notification_adapter,
    )

    try:
        dossier = await use_case.execute(
            author_id=current_user_id,
            manuscript_id=manuscript_id,
            note=note,
        )

        await session.commit()
        return dossier

    except ManuscriptNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc))

    except ManuscriptAlreadySubmittedError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


# --------------------------------------------------
# Démarrer la relecture
# --------------------------------------------------

@router.post("/dossiers/{dossier_id}/demarrer-relecture")
async def start_review(
    dossier_id: str,
    note: str | None = None,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):

    dossier_repo = SqlAlchemyEditorialDossierRepository(session)
    manuscript_repo = SqlAlchemyManuscriptRepository(session)

    notification_repo = SqlAlchemyNotificationRepository(session)
    notification_adapter = DatabaseNotificationAdapter(notification_repo)

    use_case = StartReviewUseCase(
        dossier_repo,
        manuscript_repo,
        notification_adapter,
    )

    try:
        dossier = await use_case.execute(
            dossier_id=dossier_id,
            editor_id=current_user_id,
            note=note,
        )

        await session.commit()
        return dossier

    except EditorialDossierNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc))


# --------------------------------------------------
# Demander des corrections
# --------------------------------------------------

@router.post("/dossiers/{dossier_id}/demander-corrections")
async def request_changes(
    dossier_id: str,
    note: str,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):

    dossier_repo = SqlAlchemyEditorialDossierRepository(session)
    manuscript_repo = SqlAlchemyManuscriptRepository(session)

    notification_repo = SqlAlchemyNotificationRepository(session)
    notification_adapter = DatabaseNotificationAdapter(notification_repo)

    use_case = RequestChangesUseCase(
        dossier_repo,
        manuscript_repo,
        notification_adapter,
    )

    try:
        dossier = await use_case.execute(
            dossier_id=dossier_id,
            editor_id=current_user_id,
            note=note,
        )

        await session.commit()
        return dossier

    except EditorialDossierNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc))


# --------------------------------------------------
# Accepter un manuscrit
# --------------------------------------------------

@router.post("/dossiers/{dossier_id}/accepter")
async def accept_dossier(
    dossier_id: str,
    note: str | None = None,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):

    dossier_repo = SqlAlchemyEditorialDossierRepository(session)
    manuscript_repo = SqlAlchemyManuscriptRepository(session)

    notification_repo = SqlAlchemyNotificationRepository(session)
    notification_adapter = DatabaseNotificationAdapter(notification_repo)

    use_case = AcceptDossierUseCase(
        dossier_repo,
        manuscript_repo,
        notification_adapter,
    )

    try:
        dossier = await use_case.execute(
            dossier_id=dossier_id,
            editor_id=current_user_id,
            note=note,
        )

        await session.commit()
        return dossier

    except EditorialDossierNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc))


# --------------------------------------------------
# Rejeter un manuscrit
# --------------------------------------------------

@router.post("/dossiers/{dossier_id}/rejeter")
async def reject_dossier(
    dossier_id: str,
    note: str,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):

    dossier_repo = SqlAlchemyEditorialDossierRepository(session)
    manuscript_repo = SqlAlchemyManuscriptRepository(session)

    notification_repo = SqlAlchemyNotificationRepository(session)
    notification_adapter = DatabaseNotificationAdapter(notification_repo)

    use_case = RejectDossierUseCase(
        dossier_repo,
        manuscript_repo,
        notification_adapter,
    )

    try:
        dossier = await use_case.execute(
            dossier_id=dossier_id,
            editor_id=current_user_id,
            note=note,
        )

        await session.commit()
        return dossier

    except EditorialDossierNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc))
