from datetime import datetime, timezone

from app.domain.entities.editorial_dossier import EditorialDossier


def test_editorial_dossier_creation():
    dossier = EditorialDossier(
        id="d1",
        manuscript_id="m1",
        submitted_by_user_id=4,
        assigned_editor_id=None,
        status="SUBMITTED",
        submission_note="Soumission test",
    )

    assert dossier.id == "d1"
    assert dossier.manuscript_id == "m1"
    assert dossier.status == "SUBMITTED"
    assert dossier.submission_note == "Soumission test"


def test_editorial_dossier_can_assign_editor():
    dossier = EditorialDossier(
        id="d1",
        manuscript_id="m1",
        submitted_by_user_id=4,
        assigned_editor_id=None,
        status="SUBMITTED",
    )

    dossier.assigned_editor_id = 10

    assert dossier.assigned_editor_id == 10
