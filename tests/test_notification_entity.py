from app.domain.entities.notification import Notification


def test_notification_mark_as_read_sets_fields():
    notification = Notification(
        id="n1",
        user_id=4,
        subject="Sujet",
        message="Message",
        is_read=False,
    )

    notification.mark_as_read()

    assert notification.is_read is True
    assert notification.read_at is not None
