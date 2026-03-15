from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.editorial.accept_dossier import (
    AcceptDossierUseCase,
    EditorialDossierNotFoundError as AcceptNotFoundError,
)
from app.application.use_cases.editorial.get_dossier import (
    EditorialDossierNotFoundError as GetNotFoundError,
    GetEditorialDossierUseCase,
)
from app.application.use_cases.editorial.list_dossiers import ListEditorialDossiersUseCase
from app.application.use_cases.editorial.reject_dossier import (
    EditorialDossierNotFoundError as RejectNotFoundError,
    RejectDossierUseCase,
)
from app.application.use_cases.editorial.request_changes import (
    EditorialDossierNotFoundError as ChangesNotFoundError,
    RequestChangesUseCase,
)
from app.application.use_cases.editorial.start_review import (
    EditorialDossierNotFoundError as ReviewNotFoundError,
    StartReviewUseCase,
)
from app.application.use_cases.editorial.submit_manuscript import (
    ManuscriptAlreadySubmittedError,
    ManuscriptNotFoundError,
    SubmitManuscriptUseCase,
)
from app.domain.entities.editorial_dossier import EditorialDossierError
from app.domain.entities.manuscript import ManuscriptError
from app.infrastructure.database import get_db
from app.infrastructure.repositories.editorial_dossier_sqlalchemy_repository import (
    SqlAlchemyEditorialDossierRepository,
)
from app.infrastructure.repositories.manuscript_sqlalchemy_repository import (
    SqlAlchemyManuscriptRepository,
)
from app.presentation.auth_dependencies import get_current_user_id
from app.presentation.editorial_schemas import (
    EditorialActionRequest,
    EditorialDecisionRequest,
    EditorialDossierResponse,
    SubmitManuscriptRequest,
)

router = APIRouter(prefix="/editorial", tags=["Editorial"])


@router.post(
    "/manuscrits/{manuscript_id}/soumettre",
    response_model=EditorialDossierResponse,
    status_code=status.HTTP_201_CREATED,
)
async def submit_manuscript(
    manuscript_id: str,
    request: SubmitManuscriptRequest,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    manuscript_repo = SqlAlchemyManuscriptRepository(session)
    dossier_repo = SqlAlchemyEditorialDossierRepository(session)
    use_case = SubmitManuscriptUseCase(manuscript_repo, dossier_repo)

    try:
        dossier = await use_case.execute(
            author_id=current_user_id,
            manuscript_id=manuscript_id,
            note=request.note,
        )
        await session.commit()
        return dossier
    except ManuscriptNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (ManuscriptAlreadySubmittedError, ManuscriptError, EditorialDossierError) as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/dossiers/{dossier_id}/demarrer-relecture", response_model=EditorialDossierResponse)
async def start_review(
    dossier_id: str,
    request: EditorialActionRequest,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    dossier_repo = SqlAlchemyEditorialDossierRepository(session)
    manuscript_repo = SqlAlchemyManuscriptRepository(session)
    use_case = StartReviewUseCase(dossier_repo, manuscript_repo)

    try:
        dossier = await use_case.execute(
            dossier_id=dossier_id,
            editor_id=current_user_id,
            note=request.note,
        )
        await session.commit()
        return dossier
    except ReviewNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except EditorialDossierError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/dossiers/{dossier_id}/demander-corrections", response_model=EditorialDossierResponse)
async def request_changes(
    dossier_id: str,
    request: EditorialDecisionRequest,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    dossier_repo = SqlAlchemyEditorialDossierRepository(session)
    manuscript_repo = SqlAlchemyManuscriptRepository(session)
    use_case = RequestChangesUseCase(dossier_repo, manuscript_repo)

    try:
        dossier = await use_case.execute(
            dossier_id=dossier_id,
            editor_id=current_user_id,
            note=request.note,
        )
        await session.commit()
        return dossier
    except ChangesNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except EditorialDossierError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/dossiers/{dossier_id}/accepter", response_model=EditorialDossierResponse)
async def accept_dossier(
    dossier_id: str,
    request: EditorialActionRequest,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    dossier_repo = SqlAlchemyEditorialDossierRepository(session)
    manuscript_repo = SqlAlchemyManuscriptRepository(session)
    use_case = AcceptDossierUseCase(dossier_repo, manuscript_repo)

    try:
        dossier = await use_case.execute(
            dossier_id=dossier_id,
            editor_id=current_user_id,
            note=request.note,
        )
        await session.commit()
        return dossier
    except AcceptNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except EditorialDossierError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/dossiers/{dossier_id}/rejeter", response_model=EditorialDossierResponse)
async def reject_dossier(
    dossier_id: str,
    request: EditorialDecisionRequest,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    dossier_repo = SqlAlchemyEditorialDossierRepository(session)
    manuscript_repo = SqlAlchemyManuscriptRepository(session)
    use_case = RejectDossierUseCase(dossier_repo, manuscript_repo)

    try:
        dossier = await use_case.execute(
            dossier_id=dossier_id,
            editor_id=current_user_id,
            note=request.note,
        )
        await session.commit()
        return dossier
    except RejectNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except EditorialDossierError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/dossiers", response_model=list[EditorialDossierResponse])
async def list_dossiers(
    status_filter: str | None = Query(default=None, alias="statut"),
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    dossier_repo = SqlAlchemyEditorialDossierRepository(session)
    use_case = ListEditorialDossiersUseCase(dossier_repo)
    return await use_case.execute(status=status_filter)


@router.get("/dossiers/{dossier_id}", response_model=EditorialDossierResponse)
async def get_dossier(
    dossier_id: str,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    dossier_repo = SqlAlchemyEditorialDossierRepository(session)
    use_case = GetEditorialDossierUseCase(dossier_repo)

    try:
        return await use_case.execute(dossier_id)
    except GetNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
