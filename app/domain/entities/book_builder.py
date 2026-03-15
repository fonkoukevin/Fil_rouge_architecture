import re
from datetime import datetime, timezone

from app.domain.entities.book import Book
from app.domain.entities.manuscript import Manuscript


class BookBuilderError(Exception):
    pass


class BookBuilder:
    def __init__(self) -> None:
        self._id: str | None = None
        self._manuscript_id: str | None = None
        self._author_id: int | None = None
        self._title: str | None = None
        self._synopsis: str | None = None
        self._content: str | None = None
        self._slug: str | None = None
        self._is_published: bool = True
        self._published_at: datetime = datetime.now(timezone.utc)
        self._created_at: datetime = datetime.now(timezone.utc)

    def from_manuscript(self, manuscript: Manuscript) -> "BookBuilder":
        self._manuscript_id = manuscript.id
        self._author_id = manuscript.author_id
        self._title = manuscript.title
        self._synopsis = manuscript.synopsis
        self._content = manuscript.build_snapshot_content()
        self._slug = self._build_slug(manuscript.title)
        return self

    def with_slug(self, slug: str) -> "BookBuilder":
        self._slug = slug.strip().lower()
        return self

    def with_publication_date(self, published_at: datetime) -> "BookBuilder":
        self._published_at = published_at
        return self

    def build(self) -> Book:
        if not self._manuscript_id:
            raise BookBuilderError("Le manuscript_id est obligatoire.")
        if self._author_id is None:
            raise BookBuilderError("Le author_id est obligatoire.")
        if not self._title:
            raise BookBuilderError("Le titre est obligatoire.")
        if self._content is None:
            raise BookBuilderError("Le contenu est obligatoire.")
        if not self._slug:
            raise BookBuilderError("Le slug est obligatoire.")

        return Book(
            id=self._id,
            manuscript_id=self._manuscript_id,
            author_id=self._author_id,
            title=self._title,
            synopsis=self._synopsis,
            content=self._content,
            slug=self._slug,
            is_published=self._is_published,
            published_at=self._published_at,
            created_at=self._created_at,
        )

    def _build_slug(self, title: str) -> str:
        slug = title.strip().lower()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[\s_-]+", "-", slug)
        slug = re.sub(r"^-+|-+$", "", slug)
        return slug
