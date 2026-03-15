import pytest
from datetime import datetime, timezone

from app.application.use_cases.notification.mark_notification_as_read import (
    MarkNotificationAsReadUseCase,
    NotificationNotFoundError,
)
from app.domain.entities.notification import Notification
from tests.fakes import FakeNotificationRepository


@pytest.mark.asyncio
async def test_mark_notification_as_read_sets_is_read_to_true():
    notification = Notification(
        id="n1",
        user_id=4,
        subject="Sujet",
        message="Message",
        is_read=False,
        created_at=datetime.now(timezone.utc),
        read_at=None,
    )

    repo = FakeNotificationRepository({"n1": notification})
    use_case = MarkNotificationAsReadUseCase(repo)

    updated = await use_case.execute("n1", 4)

    assert updated.is_read is True
    assert updated.read_at is not None


@pytest.mark.asyncio
async def test_mark_notification_as_read_raises_if_not_found():
    repo = FakeNotificationRepository({})
    use_case = MarkNotificationAsReadUseCase(repo)

    with pytest.raises(NotificationNotFoundError):
        await use_case.execute("unknown", 4)
