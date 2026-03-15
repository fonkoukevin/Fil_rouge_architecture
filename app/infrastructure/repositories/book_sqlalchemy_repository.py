from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.book import Book
from app.domain.repositories.book_repository import BookRepository
from app.infrastructure.models import BookModel


class SqlAlchemyBookRepository(BookRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _to_domain(self, model: BookModel) -> Book:
        return Book(
            id=model.id,
            manuscript_id=model.manuscript_id,
            author_id=model.author_id,
            title=model.title,
            synopsis=model.synopsis,
            content=model.content,
            slug=model.slug,
            is_published=model.is_published,
            published_at=model.published_at,
            created_at=model.created_at,
        )

    async def create(self, book: Book) -> Book:
        model = BookModel(
            manuscript_id=book.manuscript_id,
            author_id=book.author_id,
            title=book.title,
            synopsis=book.synopsis,
            content=book.content,
            slug=book.slug,
            is_published=book.is_published,
            published_at=book.published_at,
            created_at=book.created_at,
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, book_id: str) -> Book | None:
        stmt = select(BookModel).where(BookModel.id == book_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return None if model is None else self._to_domain(model)

    async def get_by_manuscript_id(self, manuscript_id: str) -> Book | None:
        stmt = select(BookModel).where(BookModel.manuscript_id == manuscript_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return None if model is None else self._to_domain(model)

    async def get_by_slug(self, slug: str) -> Book | None:
        stmt = select(BookModel).where(BookModel.slug == slug)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return None if model is None else self._to_domain(model)

    async def list_published(self) -> list[Book]:
        stmt = (
            select(BookModel)
            .where(BookModel.is_published.is_(True))
            .order_by(BookModel.published_at.desc())
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]

    async def search_published(self, query: str) -> list[Book]:
        like_value = f"%{query}%"
        stmt = (
            select(BookModel)
            .where(
                BookModel.is_published.is_(True),
                or_(
                    BookModel.title.ilike(like_value),
                    BookModel.synopsis.ilike(like_value),
                    BookModel.slug.ilike(like_value),
                ),
            )
            .order_by(BookModel.published_at.desc())
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]
