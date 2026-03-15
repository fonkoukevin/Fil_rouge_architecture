from datetime import datetime, timezone

from app.domain.entities.editorial_dossier import EditorialDossierError
from app.domain.ports.notification_port import NotificationPort
from app.domain.repositories.editorial_dossier_repository import EditorialDossierRepository
from app.domain.repositories.manuscript_repository import ManuscriptRepository


class EditorialDossierNotFoundError(Exception):
    pass


class StartReviewUseCase:
    def __init__(
        self,
        dossier_repository: EditorialDossierRepository,
        manuscript_repository: ManuscriptRepository,
        notification_port: NotificationPort,
    ) -> None:
        self.dossier_repository = dossier_repository
        self.manuscript_repository = manuscript_repository
        self.notification_port = notification_port

    async def execute(self, dossier_id: str, editor_id: int, note: str | None):
        dossier = await self.dossier_repository.get_by_id(dossier_id)
        if dossier is None:
            raise EditorialDossierNotFoundError("Dossier éditorial introuvable.")

        dossier.start_review(editor_id=editor_id, note=note)

        manuscript = await self.manuscript_repository.get_by_id_and_author_id(
            dossier.manuscript_id,
            dossier.submitted_by_user_id,
        )
        if manuscript is not None:
            manuscript.status = "IN_REVIEW"
            manuscript.updated_at = datetime.now(timezone.utc)
            await self.manuscript_repository.update_manuscript(manuscript)

        updated_dossier = await self.dossier_repository.update(dossier)

        if manuscript is not None:
            await self.notification_port.send(
                user_id=manuscript.author_id,
                subject="Relecture démarrée",
                message=f"La relecture de votre manuscrit '{manuscript.title}' a commencé.",
            )

        return updated_dossier
