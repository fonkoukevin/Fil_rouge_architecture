from app.domain.entities.book_builder import BookBuilder, BookBuilderError
from app.domain.repositories.book_repository import BookRepository
from app.domain.repositories.manuscript_repository import ManuscriptRepository


class PublicationError(Exception):
    pass


class ManuscriptNotFoundError(Exception):
    pass


class PublishManuscriptUseCase:
    def __init__(
        self,
        manuscript_repository: ManuscriptRepository,
        book_repository: BookRepository,
    ) -> None:
        self.manuscript_repository = manuscript_repository
        self.book_repository = book_repository

    async def execute(self, manuscript_id: str, current_user_id: int):
        manuscript = await self.manuscript_repository.get_by_id_and_author_id(
            manuscript_id=manuscript_id,
            author_id=current_user_id,
        )

        if manuscript is None:
            raise ManuscriptNotFoundError("Manuscrit introuvable.")

        if manuscript.status != "ACCEPTED":
            raise PublicationError("Seul un manuscrit accepté peut être publié.")

        existing_book = await self.book_repository.get_by_manuscript_id(manuscript_id)
        if existing_book is not None:
            raise PublicationError("Ce manuscrit a déjà été publié.")

        book = BookBuilder().from_manuscript(manuscript).build()

        existing_slug = await self.book_repository.get_by_slug(book.slug)
        if existing_slug is not None:
            raise PublicationError("Un livre avec ce slug existe déjà.")

        return await self.book_repository.create(book)
