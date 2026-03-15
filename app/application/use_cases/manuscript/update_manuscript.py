from app.application.use_cases.manuscript.get_manuscript import ManuscriptNotFoundError
from app.domain.entities.manuscript import ManuscriptError
from app.domain.repositories.manuscript_repository import ManuscriptRepository


class UpdateManuscriptUseCase:
    def __init__(self, repository: ManuscriptRepository) -> None:
        self.repository = repository

    async def execute(self, author_id: str, manuscript_id: str, title: str, synopsis: str | None):
        manuscript = await self.repository.get_by_id_and_author_id(manuscript_id, author_id)
        if manuscript is None:
            raise ManuscriptNotFoundError("Manuscrit introuvable.")

        manuscript.update_metadata(title, synopsis)
        return await self.repository.update_manuscript(manuscript)
