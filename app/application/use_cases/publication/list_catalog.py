from app.domain.repositories.book_repository import BookRepository


class ListCatalogUseCase:
    def __init__(self, book_repository: BookRepository) -> None:
        self.book_repository = book_repository

    async def execute(self):
        return await self.book_repository.list_published()
