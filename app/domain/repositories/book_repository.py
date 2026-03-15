from abc import ABC, abstractmethod

from app.domain.entities.book import Book


class BookRepository(ABC):
    @abstractmethod
    async def create(self, book: Book) -> Book:
        pass

    @abstractmethod
    async def get_by_id(self, book_id: str) -> Book | None:
        pass

    @abstractmethod
    async def get_by_manuscript_id(self, manuscript_id: str) -> Book | None:
        pass

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Book | None:
        pass

    @abstractmethod
    async def list_published(self) -> list[Book]:
        pass

    @abstractmethod
    async def search_published(self, query: str) -> list[Book]:
        pass
