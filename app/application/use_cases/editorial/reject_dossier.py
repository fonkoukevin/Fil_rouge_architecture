from datetime import datetime, timezone

from app.domain.repositories.editorial_dossier_repository import EditorialDossierRepository
from app.domain.repositories.manuscript_repository import ManuscriptRepository


class EditorialDossierNotFoundError(Exception):
    pass


class RejectDossierUseCase:
    def __init__(
        self,
        dossier_repository: EditorialDossierRepository,
        manuscript_repository: ManuscriptRepository,
    ) -> None:
        self.dossier_repository = dossier_repository
        self.manuscript_repository = manuscript_repository

    async def execute(self, dossier_id: str, editor_id: int, note: str):
        dossier = await self.dossier_repository.get_by_id(dossier_id)
        if dossier is None:
            raise EditorialDossierNotFoundError("Dossier éditorial introuvable.")

        dossier.reject(editor_id=editor_id, note=note)

        manuscript = await self.manuscript_repository.get_by_id_and_author_id(
            dossier.manuscript_id, dossier.submitted_by_user_id
        )
        if manuscript is not None:
            manuscript.status = "REJECTED"
            manuscript.updated_at = datetime.now(timezone.utc)
            await self.manuscript_repository.update_manuscript(manuscript)

        return await self.dossier_repository.update(dossier)
