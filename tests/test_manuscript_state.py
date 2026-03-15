import pytest
from datetime import datetime, timezone

from app.domain.entities.manuscript import Manuscript, ManuscriptError


def build_manuscript(status="DRAFT"):
    return Manuscript(
        id="m1",
        author_id=4,
        title="Titre",
        synopsis="Synopsis",
        status=status,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        chapters=[],
    )


def test_draft_manuscript_can_be_submitted():
    manuscript = build_manuscript("DRAFT")

    manuscript.submit()

    assert manuscript.status == "SUBMITTED"


def test_submitted_manuscript_cannot_be_updated():
    manuscript = build_manuscript("SUBMITTED")

    with pytest.raises(ManuscriptError):
        manuscript.update_metadata("Nouveau titre", "Nouveau synopsis")
