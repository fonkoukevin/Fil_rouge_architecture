from datetime import datetime, timezone

from app.application.use_cases.manuscript.get_manuscript import ManuscriptNotFoundError
from app.domain.entities.manuscript_version import ManuscriptVersion
from app.domain.repositories.manuscript_repository import ManuscriptRepository


class CreateVersionUseCase:
    def __init__(self, repository: ManuscriptRepository) -> None:
        self.repository = repository

    async def execute(self, author_id: str, manuscript_id: str) -> ManuscriptVersion:
        manuscript = await self.repository.get_by_id_and_author_id(manuscript_id, author_id)
        if manuscript is None:
            raise ManuscriptNotFoundError("Manuscrit introuvable.")

        next_version = await self.repository.get_next_version_number(manuscript_id)

        version = ManuscriptVersion(
            id=None,
            manuscript_id=manuscript.id,
            version_number=next_version,
            title_snapshot=manuscript.title,
            synopsis_snapshot=manuscript.synopsis,
            content_snapshot=manuscript.build_snapshot_content(),
            created_at=datetime.now(timezone.utc),
        )

        return await self.repository.create_version(version)
