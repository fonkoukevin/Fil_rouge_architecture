from __future__ import annotations
from abc import ABC, abstractmethod

from app.domain.entities.chapter import Chapter
from app.domain.entities.manuscript import Manuscript
from app.domain.entities.manuscript_version import ManuscriptVersion


class ManuscriptRepository(ABC):
    @abstractmethod
    async def create_manuscript(self, manuscript: Manuscript) -> Manuscript:
        pass

    @abstractmethod
    async def list_by_author_id(self, author_id: int) -> list[Manuscript]:
        pass

    @abstractmethod
    async def get_by_id_and_author_id(self, manuscript_id: str, author_id: int) -> Manuscript | None:
        pass

    @abstractmethod
    async def update_manuscript(self, manuscript: Manuscript) -> Manuscript:
        pass

    @abstractmethod
    async def add_chapter(self, chapter: Chapter) -> Chapter:
        pass

    @abstractmethod
    async def get_chapter_by_id(self, chapter_id: str) -> Chapter | None:
        pass

    @abstractmethod
    async def update_chapter(self, chapter: Chapter) -> Chapter:
        pass

    @abstractmethod
    async def get_next_chapter_order(self, manuscript_id: str) -> int:
        pass

    @abstractmethod
    async def create_version(self, version: ManuscriptVersion) -> ManuscriptVersion:
        pass

    @abstractmethod
    async def get_next_version_number(self, manuscript_id: str) -> int:
        pass
