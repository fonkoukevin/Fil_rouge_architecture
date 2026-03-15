import pytest
from datetime import datetime, timezone

from app.application.use_cases.publication.publish_manuscript import (
    PublishManuscriptUseCase,
    PublicationError,
    ManuscriptNotFoundError,
)
from app.domain.entities.manuscript import Manuscript
from tests.fakes import (
    FakeBookRepository,
    FakeManuscriptRepository,
    FakeNotificationPort,
)


def build_manuscript(status="ACCEPTED"):
    return Manuscript(
        id="m1",
        author_id=4,
        title="Mon Roman de Test",
        synopsis="Synopsis",
        status=status,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        chapters=[],
    )


@pytest.mark.asyncio
async def test_publish_manuscript_creates_book_and_notification():
    manuscript = build_manuscript("ACCEPTED")
    manuscript_repo = FakeManuscriptRepository({"m1": manuscript})
    book_repo = FakeBookRepository()
    notification_port = FakeNotificationPort()

    use_case = PublishManuscriptUseCase(
        manuscript_repo,
        book_repo,
        notification_port,
    )

    book = await use_case.execute(
        manuscript_id="m1",
        current_user_id=4,
    )

    assert book.manuscript_id == "m1"
    assert book.slug == "mon-roman-de-test"
    assert len(book_repo.created) == 1
    assert len(notification_port.sent) == 1
    assert notification_port.sent[0]["subject"] == "Livre publié"


@pytest.mark.asyncio
async def test_publish_manuscript_raises_if_manuscript_not_found():
    manuscript_repo = FakeManuscriptRepository({})
    book_repo = FakeBookRepository()
    notification_port = FakeNotificationPort()

    use_case = PublishManuscriptUseCase(
        manuscript_repo,
        book_repo,
        notification_port,
    )

    with pytest.raises(ManuscriptNotFoundError):
        await use_case.execute("m1", 4)


@pytest.mark.asyncio
async def test_publish_manuscript_raises_if_manuscript_not_accepted():
    manuscript = build_manuscript("SUBMITTED")
    manuscript_repo = FakeManuscriptRepository({"m1": manuscript})
    book_repo = FakeBookRepository()
    notification_port = FakeNotificationPort()

    use_case = PublishManuscriptUseCase(
        manuscript_repo,
        book_repo,
        notification_port,
    )

    with pytest.raises(PublicationError):
        await use_case.execute("m1", 4)
