from app.domain.repositories.book_repository import BookRepository


class BookNotFoundError(Exception):
    pass


class GetBookUseCase:
    def __init__(self, book_repository: BookRepository) -> None:
        self.book_repository = book_repository

    async def execute(self, book_id: str):
        book = await self.book_repository.get_by_id(book_id)
        if book is None:
            raise BookNotFoundError("Livre introuvable.")
        return book
