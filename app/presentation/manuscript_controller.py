from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.manuscript.add_chapter import AddChapterUseCase
from app.application.use_cases.manuscript.create_manuscript import CreateManuscriptUseCase
from app.application.use_cases.manuscript.create_version import CreateVersionUseCase
from app.application.use_cases.manuscript.get_manuscript import (
    GetManuscriptUseCase,
    ManuscriptNotFoundError,
)
from app.application.use_cases.manuscript.list_manuscripts import ListManuscriptsUseCase
from app.application.use_cases.manuscript.update_chapter import (
    ChapterNotFoundError,
    UpdateChapterUseCase,
)
from app.application.use_cases.manuscript.update_manuscript import UpdateManuscriptUseCase
from app.domain.entities.manuscript import ManuscriptError
from app.infrastructure.database import get_db
from app.infrastructure.repositories.manuscript_sqlalchemy_repository import (
    SqlAlchemyManuscriptRepository,
)
from app.presentation.auth_dependencies import get_current_user_id
from app.presentation.manuscript_schemas import (
    ChapterResponse,
    CreateChapterRequest,
    CreateManuscriptRequest,
    ManuscriptDetailsResponse,
    ManuscriptResponse,
    ManuscriptVersionResponse,
    UpdateChapterRequest,
    UpdateManuscriptRequest,
)

router = APIRouter(prefix="/manuscrits", tags=["Manuscrits"])


@router.post("", response_model=ManuscriptResponse, status_code=status.HTTP_201_CREATED)
async def create_manuscript(
    request: CreateManuscriptRequest,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    repository = SqlAlchemyManuscriptRepository(session)
    use_case = CreateManuscriptUseCase(repository)

    manuscript = await use_case.execute(
        author_id=current_user_id,
        title=request.title,
        synopsis=request.synopsis,
    )

    await session.commit()
    return manuscript


@router.get("", response_model=list[ManuscriptResponse])
async def list_manuscripts(
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    repository = SqlAlchemyManuscriptRepository(session)
    use_case = ListManuscriptsUseCase(repository)

    manuscripts = await use_case.execute(author_id=current_user_id)
    return manuscripts


@router.get("/{manuscript_id}", response_model=ManuscriptDetailsResponse)
async def get_manuscript(
    manuscript_id: str,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    repository = SqlAlchemyManuscriptRepository(session)
    use_case = GetManuscriptUseCase(repository)

    try:
        manuscript = await use_case.execute(
            author_id=current_user_id,
            manuscript_id=manuscript_id,
        )
        return manuscript
    except ManuscriptNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.put("/{manuscript_id}", response_model=ManuscriptResponse)
async def update_manuscript(
    manuscript_id: str,
    request: UpdateManuscriptRequest,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    repository = SqlAlchemyManuscriptRepository(session)
    use_case = UpdateManuscriptUseCase(repository)

    try:
        manuscript = await use_case.execute(
            author_id=current_user_id,
            manuscript_id=manuscript_id,
            title=request.title,
            synopsis=request.synopsis,
        )
        await session.commit()
        return manuscript
    except ManuscriptNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ManuscriptError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{manuscript_id}/chapitres", response_model=ChapterResponse, status_code=status.HTTP_201_CREATED)
async def add_chapter(
    manuscript_id: str,
    request: CreateChapterRequest,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    repository = SqlAlchemyManuscriptRepository(session)
    use_case = AddChapterUseCase(repository)

    try:
        chapter = await use_case.execute(
            author_id=current_user_id,
            manuscript_id=manuscript_id,
            title=request.title,
            content=request.content,
        )
        await session.commit()
        return chapter
    except ManuscriptNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ManuscriptError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/{manuscript_id}/chapitres/{chapter_id}", response_model=ChapterResponse)
async def update_chapter(
    manuscript_id: str,
    chapter_id: str,
    request: UpdateChapterRequest,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    repository = SqlAlchemyManuscriptRepository(session)
    use_case = UpdateChapterUseCase(repository)

    try:
        chapter = await use_case.execute(
            author_id=current_user_id,
            manuscript_id=manuscript_id,
            chapter_id=chapter_id,
            title=request.title,
            content=request.content,
        )
        await session.commit()
        return chapter
    except ManuscriptNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ChapterNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{manuscript_id}/versions", response_model=ManuscriptVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_version(
    manuscript_id: str,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    repository = SqlAlchemyManuscriptRepository(session)
    use_case = CreateVersionUseCase(repository)

    try:
        version = await use_case.execute(
            author_id=current_user_id,
            manuscript_id=manuscript_id,
        )
        await session.commit()
        return version
    except ManuscriptNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
