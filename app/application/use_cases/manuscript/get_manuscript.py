from app.domain.repositories.manuscript_repository import ManuscriptRepository
from app.domain.entities.manuscript import Manuscript


class ManuscriptNotFoundError(Exception):
    pass


class GetManuscriptUseCase:
    def __init__(self, repository: ManuscriptRepository) -> None:
        self.repository = repository

    async def execute(self, author_id: str, manuscript_id: str) -> Manuscript:
        manuscript = await self.repository.get_by_id_and_author_id(manuscript_id, author_id)
        if manuscript is None:
            raise ManuscriptNotFoundError("Manuscrit introuvable.")
        return manuscript
