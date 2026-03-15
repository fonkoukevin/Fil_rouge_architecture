import pytest
from datetime import datetime, timezone

from app.application.use_cases.editorial.submit_manuscript import (
    SubmitManuscriptUseCase,
    ManuscriptAlreadySubmittedError,
    ManuscriptNotFoundError,
)
from app.domain.entities.editorial_dossier import EditorialDossier
from app.domain.entities.manuscript import Manuscript
from tests.fakes import (
    FakeEditorialDossierRepository,
    FakeManuscriptRepository,
    FakeNotificationPort,
)


def build_manuscript(status="DRAFT"):
    return Manuscript(
        id="m1",
        author_id=4,
        title="Mon roman",
        synopsis="Synopsis",
        status=status,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        chapters=[],
    )


@pytest.mark.asyncio
async def test_submit_manuscript_creates_editorial_dossier_and_notification():
    manuscript = build_manuscript("DRAFT")

    manuscript_repo = FakeManuscriptRepository({"m1": manuscript})
    dossier_repo = FakeEditorialDossierRepository()
    notification_port = FakeNotificationPort()

    use_case = SubmitManuscriptUseCase(
        manuscript_repo,
        dossier_repo,
        notification_port,
    )

    dossier = await use_case.execute(
        author_id=4,
        manuscript_id="m1",
        note="Soumission test",
    )

    assert dossier.status == "SUBMITTED"
    assert manuscript.status == "SUBMITTED"
    assert len(dossier_repo.created) == 1
    assert len(notification_port.sent) == 1
    assert notification_port.sent[0]["subject"] == "Manuscrit soumis"


@pytest.mark.asyncio
async def test_submit_manuscript_raises_if_not_found():
    manuscript_repo = FakeManuscriptRepository({})
    dossier_repo = FakeEditorialDossierRepository()
    notification_port = FakeNotificationPort()

    use_case = SubmitManuscriptUseCase(
        manuscript_repo,
        dossier_repo,
        notification_port,
    )

    with pytest.raises(ManuscriptNotFoundError):
        await use_case.execute(author_id=4, manuscript_id="unknown", note=None)


@pytest.mark.asyncio
async def test_submit_manuscript_raises_if_active_dossier_exists():
    manuscript = build_manuscript("DRAFT")
    existing_dossier = EditorialDossier(
        id="d1",
        manuscript_id="m1",
        submitted_by_user_id=4,
        assigned_editor_id=None,
        status="SUBMITTED",
    )

    manuscript_repo = FakeManuscriptRepository({"m1": manuscript})
    dossier_repo = FakeEditorialDossierRepository(
        dossiers_by_manuscript_id={"m1": existing_dossier}
    )
    notification_port = FakeNotificationPort()

    use_case = SubmitManuscriptUseCase(
        manuscript_repo,
        dossier_repo,
        notification_port,
    )

    with pytest.raises(ManuscriptAlreadySubmittedError):
        await use_case.execute(author_id=4, manuscript_id="m1", note=None)
