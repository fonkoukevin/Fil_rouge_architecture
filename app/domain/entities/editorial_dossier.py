from dataclasses import dataclass, field
from datetime import datetime, timezone


class EditorialDossierError(Exception):
    pass


@dataclass
class EditorialDossier:
    id: str | None
    manuscript_id: str
    submitted_by_user_id: int
    assigned_editor_id: int | None
    status: str = "SUBMITTED"
    submission_note: str | None = None
    editorial_note: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def start_review(self, editor_id: int, note: str | None = None) -> None:
        if self.status not in {"SUBMITTED", "CHANGES_REQUESTED"}:
            raise EditorialDossierError(
                "Impossible de démarrer la relecture depuis cet état."
            )
        self.assigned_editor_id = editor_id
        self.status = "IN_REVIEW"
        self.editorial_note = note
        self.updated_at = datetime.now(timezone.utc)

    def request_changes(self, editor_id: int, note: str) -> None:
        if self.status != "IN_REVIEW":
            raise EditorialDossierError(
                "Impossible de demander des corrections si le dossier n'est pas en relecture."
            )
        self.assigned_editor_id = editor_id
        self.status = "CHANGES_REQUESTED"
        self.editorial_note = note.strip()
        self.updated_at = datetime.now(timezone.utc)

    def accept(self, editor_id: int, note: str | None = None) -> None:
        if self.status != "IN_REVIEW":
            raise EditorialDossierError(
                "Impossible d'accepter un dossier qui n'est pas en relecture."
            )
        self.assigned_editor_id = editor_id
        self.status = "ACCEPTED"
        self.editorial_note = note
        self.updated_at = datetime.now(timezone.utc)

    def reject(self, editor_id: int, note: str) -> None:
        if self.status not in {"SUBMITTED", "IN_REVIEW", "CHANGES_REQUESTED"}:
            raise EditorialDossierError(
                "Impossible de rejeter le dossier depuis cet état."
            )
        self.assigned_editor_id = editor_id
        self.status = "REJECTED"
        self.editorial_note = note.strip()
        self.updated_at = datetime.now(timezone.utc)
