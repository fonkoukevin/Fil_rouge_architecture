from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.publication.get_book import (
    BookNotFoundError,
    GetBookUseCase,
)
from app.application.use_cases.publication.list_catalog import ListCatalogUseCase
from app.application.use_cases.publication.publish_manuscript import (
    ManuscriptNotFoundError,
    PublicationError,
    PublishManuscriptUseCase,
)
from app.application.use_cases.publication.search_catalog import SearchCatalogUseCase
from app.infrastructure.database import get_db
from app.infrastructure.repositories.book_sqlalchemy_repository import (
    SqlAlchemyBookRepository,
)
from app.infrastructure.repositories.manuscript_sqlalchemy_repository import (
    SqlAlchemyManuscriptRepository,
)
from app.presentation.auth_dependencies import get_current_user_id
from app.presentation.publication_schemas import (
    BookResponse,
    PublishManuscriptRequest,
)

router = APIRouter(tags=["Publication"])


@router.post("/publications", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def publish_manuscript(
    request: PublishManuscriptRequest,
    session: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    manuscript_repo = SqlAlchemyManuscriptRepository(session)
    book_repo = SqlAlchemyBookRepository(session)
    use_case = PublishManuscriptUseCase(manuscript_repo, book_repo)

    try:
        book = await use_case.execute(
            manuscript_id=request.manuscript_id,
            current_user_id=current_user_id,
        )
        await session.commit()
        return book
    except ManuscriptNotFoundError as exc:
        await session.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PublicationError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/livres/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: str,
    session: AsyncSession = Depends(get_db),
):
    book_repo = SqlAlchemyBookRepository(session)
    use_case = GetBookUseCase(book_repo)

    try:
        return await use_case.execute(book_id)
    except BookNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/catalogue", response_model=list[BookResponse])
async def list_catalog(
    session: AsyncSession = Depends(get_db),
):
    book_repo = SqlAlchemyBookRepository(session)
    use_case = ListCatalogUseCase(book_repo)
    return await use_case.execute()


@router.get("/catalogue/recherche", response_model=list[BookResponse])
async def search_catalog(
    q: str = Query(..., min_length=1),
    session: AsyncSession = Depends(get_db),
):
    book_repo = SqlAlchemyBookRepository(session)
    use_case = SearchCatalogUseCase(book_repo)
    return await use_case.execute(q)
