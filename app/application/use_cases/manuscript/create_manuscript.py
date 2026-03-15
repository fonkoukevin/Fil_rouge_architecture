from app.domain.entities.manuscript import Manuscript
from app.domain.repositories.manuscript_repository import ManuscriptRepository


class CreateManuscriptUseCase:
    def __init__(self, repository: ManuscriptRepository) -> None:
        self.repository = repository

    async def execute(self, author_id: int, title: str, synopsis: str | None) -> Manuscript:
        manuscript = Manuscript(
            id=None,
            author_id=author_id,
            title=title.strip(),
            synopsis=synopsis.strip() if synopsis else None,
        )
        return await self.repository.create_manuscript(manuscript)
