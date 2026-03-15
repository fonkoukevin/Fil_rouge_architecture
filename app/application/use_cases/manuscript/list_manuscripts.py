from app.domain.repositories.manuscript_repository import ManuscriptRepository
from app.domain.entities.manuscript import Manuscript


class ListManuscriptsUseCase:
    def __init__(self, repository: ManuscriptRepository) -> None:
        self.repository = repository

    async def execute(self, author_id: str) -> list[Manuscript]:
        return await self.repository.list_by_author_id(author_id)
