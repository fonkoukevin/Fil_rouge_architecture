from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.chapter import Chapter
from app.domain.entities.manuscript import Manuscript
from app.domain.entities.manuscript_version import ManuscriptVersion
from app.domain.repositories.manuscript_repository import ManuscriptRepository
from app.infrastructure.models import ChapterModel, ManuscriptModel, ManuscriptVersionModel


class SqlAlchemyManuscriptRepository(ManuscriptRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _to_domain_chapter(self, model: ChapterModel) -> Chapter:
        return Chapter(
            id=model.id,
            manuscript_id=model.manuscript_id,
            title=model.title,
            content=model.content,
            chapter_order=model.chapter_order,
        )

    def _to_domain_manuscript(self, model: ManuscriptModel) -> Manuscript:
        raw_chapters = model.__dict__.get("chapters", [])
        chapters = [
            self._to_domain_chapter(chapter)
            for chapter in sorted(raw_chapters, key=lambda ch: ch.chapter_order)
        ]

        return Manuscript(
            id=model.id,
            author_id=model.author_id,
            title=model.title,
            synopsis=model.synopsis,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
            chapters=chapters,
        )

    async def create_manuscript(self, manuscript: Manuscript) -> Manuscript:
        model = ManuscriptModel(
            author_id=manuscript.author_id,
            title=manuscript.title,
            synopsis=manuscript.synopsis,
            status=manuscript.status,
            created_at=manuscript.created_at,
            updated_at=manuscript.updated_at,
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)

        return Manuscript(
            id=model.id,
            author_id=model.author_id,
            title=model.title,
            synopsis=model.synopsis,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
            chapters=[],
        )

    async def list_by_author_id(self, author_id: int) -> list[Manuscript]:
        stmt = (
            select(ManuscriptModel)
            .where(ManuscriptModel.author_id == author_id)
            .options(selectinload(ManuscriptModel.chapters))
            .order_by(ManuscriptModel.created_at.desc())
        )
        result = await self.session.execute(stmt)
        models = result.scalars().unique().all()
        return [self._to_domain_manuscript(model) for model in models]

    async def get_by_id_and_author_id(self, manuscript_id: str, author_id: int) -> Manuscript | None:
        stmt = (
            select(ManuscriptModel)
            .where(
                ManuscriptModel.id == manuscript_id,
                ManuscriptModel.author_id == author_id,
            )
            .options(
                selectinload(ManuscriptModel.chapters),
                selectinload(ManuscriptModel.versions),
            )
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain_manuscript(model)

    async def update_manuscript(self, manuscript: Manuscript) -> Manuscript:
        stmt = (
            select(ManuscriptModel)
            .where(ManuscriptModel.id == manuscript.id)
            .options(selectinload(ManuscriptModel.chapters))
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one()

        model.title = manuscript.title
        model.synopsis = manuscript.synopsis
        model.status = manuscript.status
        model.updated_at = manuscript.updated_at

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain_manuscript(model)

    async def add_chapter(self, chapter: Chapter) -> Chapter:
        model = ChapterModel(
            manuscript_id=chapter.manuscript_id,
            title=chapter.title,
            content=chapter.content,
            chapter_order=chapter.chapter_order,
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain_chapter(model)

    async def get_chapter_by_id(self, chapter_id: str) -> Chapter | None:
        stmt = select(ChapterModel).where(ChapterModel.id == chapter_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain_chapter(model)

    async def update_chapter(self, chapter: Chapter) -> Chapter:
        stmt = select(ChapterModel).where(ChapterModel.id == chapter.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one()

        model.title = chapter.title
        model.content = chapter.content

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain_chapter(model)

    async def get_next_chapter_order(self, manuscript_id: str) -> int:
        stmt = select(func.max(ChapterModel.chapter_order)).where(
            ChapterModel.manuscript_id == manuscript_id
        )
        result = await self.session.execute(stmt)
        max_order = result.scalar_one_or_none()
        return 1 if max_order is None else max_order + 1

    async def create_version(self, version: ManuscriptVersion) -> ManuscriptVersion:
        model = ManuscriptVersionModel(
            manuscript_id=version.manuscript_id,
            version_number=version.version_number,
            title_snapshot=version.title_snapshot,
            synopsis_snapshot=version.synopsis_snapshot,
            content_snapshot=version.content_snapshot,
            created_at=version.created_at,
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)

        return ManuscriptVersion(
            id=model.id,
            manuscript_id=model.manuscript_id,
            version_number=model.version_number,
            title_snapshot=model.title_snapshot,
            synopsis_snapshot=model.synopsis_snapshot,
            content_snapshot=model.content_snapshot,
            created_at=model.created_at,
        )

    async def get_next_version_number(self, manuscript_id: str) -> int:
        stmt = select(func.max(ManuscriptVersionModel.version_number)).where(
            ManuscriptVersionModel.manuscript_id == manuscript_id
        )
        result = await self.session.execute(stmt)
        max_version = result.scalar_one_or_none()
        return 1 if max_version is None else max_version + 1
