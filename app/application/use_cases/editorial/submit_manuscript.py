from app.domain.entities.editorial_dossier import EditorialDossier
from app.domain.repositories.editorial_dossier_repository import EditorialDossierRepository
from app.domain.repositories.manuscript_repository import ManuscriptRepository
from app.domain.ports.notification_port import NotificationPort


class ManuscriptAlreadySubmittedError(Exception):
    pass


class ManuscriptNotFoundError(Exception):
    pass


class SubmitManuscriptUseCase:
    def __init__(
        self,
        manuscript_repository: ManuscriptRepository,
        dossier_repository: EditorialDossierRepository,
        notification_port: NotificationPort,
    ) -> None:
        self.manuscript_repository = manuscript_repository
        self.dossier_repository = dossier_repository
        self.notification_port = notification_port

    async def execute(self, author_id: int, manuscript_id: str, note: str | None) -> EditorialDossier:
        manuscript = await self.manuscript_repository.get_by_id_and_author_id(
            manuscript_id,
            author_id,
        )
        if manuscript is None:
            raise ManuscriptNotFoundError("Manuscrit introuvable.")

        existing = await self.dossier_repository.get_by_manuscript_id(manuscript_id)
        if existing and existing.status in {"SUBMITTED", "IN_REVIEW", "ACCEPTED"}:
            raise ManuscriptAlreadySubmittedError(
                "Ce manuscrit possède déjà un dossier éditorial actif."
            )

        manuscript.submit()
        await self.manuscript_repository.update_manuscript(manuscript)

        dossier = EditorialDossier(
            id=None,
            manuscript_id=manuscript.id,
            submitted_by_user_id=author_id,
            assigned_editor_id=None,
            status="SUBMITTED",
            submission_note=note.strip() if note else None,
        )

        if existing and existing.status in {"CHANGES_REQUESTED", "REJECTED"}:
            existing.status = "SUBMITTED"
            existing.submission_note = note.strip() if note else None
            existing.editorial_note = None
            existing.updated_at = dossier.updated_at
            existing.assigned_editor_id = None

            updated_dossier = await self.dossier_repository.update(existing)

            await self.notification_port.send(
                user_id=author_id,
                subject="Manuscrit re-soumis",
                message=f"Votre manuscrit '{manuscript.title}' a été re-soumis à l’édition.",
            )

            return updated_dossier

        created_dossier = await self.dossier_repository.create(dossier)

        await self.notification_port.send(
            user_id=author_id,
            subject="Manuscrit soumis",
            message=f"Votre manuscrit '{manuscript.title}' a bien été soumis à l’édition.",
        )

        return created_dossier