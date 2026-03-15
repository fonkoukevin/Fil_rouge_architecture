from app.domain.repositories.book_repository import BookRepository


class SearchCatalogUseCase:
    def __init__(self, book_repository: BookRepository) -> None:
        self.book_repository = book_repository

    async def execute(self, query: str):
        return await self.book_repository.search_published(query)
