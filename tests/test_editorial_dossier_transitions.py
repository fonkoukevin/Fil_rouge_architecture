import pytest

from app.domain.entities.editorial_dossier import EditorialDossier, EditorialDossierError


def build_dossier(status="SUBMITTED"):
    return EditorialDossier(
        id="d1",
        manuscript_id="m1",
        submitted_by_user_id=4,
        assigned_editor_id=None,
        status=status,
        submission_note="Soumission",
        editorial_note=None,
    )


def test_start_review_updates_status_editor_and_note():
    dossier = build_dossier("SUBMITTED")

    dossier.start_review(editor_id=10, note="Début relecture")

    assert dossier.status == "IN_REVIEW"
    assert dossier.assigned_editor_id == 10
    assert dossier.editorial_note == "Début relecture"


def test_request_changes_updates_status_and_note():
    dossier = build_dossier("IN_REVIEW")
    dossier.assigned_editor_id = 10

    dossier.request_changes(editor_id=10, note="Merci de corriger le chapitre 2")

    assert dossier.status == "CHANGES_REQUESTED"
    assert dossier.editorial_note == "Merci de corriger le chapitre 2"


def test_accept_updates_status():
    dossier = build_dossier("IN_REVIEW")
    dossier.assigned_editor_id = 10

    dossier.accept(editor_id=10, note="Validé")

    assert dossier.status == "ACCEPTED"
    assert dossier.editorial_note == "Validé"


def test_reject_updates_status():
    dossier = build_dossier("IN_REVIEW")
    dossier.assigned_editor_id = 10

    dossier.reject(editor_id=10, note="Non retenu")

    assert dossier.status == "REJECTED"
    assert dossier.editorial_note == "Non retenu"


def test_cannot_accept_if_not_in_review():
    dossier = build_dossier("SUBMITTED")

    with pytest.raises(EditorialDossierError):
        dossier.accept(editor_id=10, note="Impossible")
