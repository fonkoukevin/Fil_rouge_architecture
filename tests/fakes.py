from app.domain.entities.editorial_dossier import EditorialDossier
from app.domain.entities.manuscript import Manuscript
from app.domain.entities.notification import Notification
from app.domain.entities.book import Book


class FakeManuscriptRepository:
    def __init__(self, manuscripts=None):
        self.manuscripts = manuscripts or {}
        self.updated_manuscripts = []

    async def get_by_id_and_author_id(self, manuscript_id: str, author_id: int):
        manuscript = self.manuscripts.get(manuscript_id)
        if manuscript and manuscript.author_id == author_id:
            return manuscript
        return None

    async def update_manuscript(self, manuscript: Manuscript):
        self.manuscripts[manuscript.id] = manuscript
        self.updated_manuscripts.append(manuscript)
        return manuscript


class FakeEditorialDossierRepository:
    def __init__(self, dossiers_by_manuscript_id=None, dossiers_by_id=None):
        self.dossiers_by_manuscript_id = dossiers_by_manuscript_id or {}
        self.dossiers_by_id = dossiers_by_id or {}
        self.created = []
        self.updated = []

    async def get_by_manuscript_id(self, manuscript_id: str):
        return self.dossiers_by_manuscript_id.get(manuscript_id)

    async def create(self, dossier: EditorialDossier):
        dossier.id = dossier.id or "dossier-1"
        self.created.append(dossier)
        self.dossiers_by_manuscript_id[dossier.manuscript_id] = dossier
        self.dossiers_by_id[dossier.id] = dossier
        return dossier

    async def update(self, dossier: EditorialDossier):
        self.updated.append(dossier)
        self.dossiers_by_manuscript_id[dossier.manuscript_id] = dossier
        self.dossiers_by_id[dossier.id] = dossier
        return dossier

    async def get_by_id(self, dossier_id: str):
        return self.dossiers_by_id.get(dossier_id)


class FakeNotificationPort:
    def __init__(self):
        self.sent = []

    async def send(self, user_id: int, subject: str, message: str) -> None:
        self.sent.append(
            {
                "user_id": user_id,
                "subject": subject,
                "message": message,
            }
        )


class FakeBookRepository:
    def __init__(self, books_by_manuscript_id=None, books_by_slug=None):
        self.books_by_manuscript_id = books_by_manuscript_id or {}
        self.books_by_slug = books_by_slug or {}
        self.created = []

    async def get_by_manuscript_id(self, manuscript_id: str):
        return self.books_by_manuscript_id.get(manuscript_id)

    async def get_by_slug(self, slug: str):
        return self.books_by_slug.get(slug)

    async def create(self, book: Book):
        book.id = book.id or "book-1"
        self.created.append(book)
        self.books_by_manuscript_id[book.manuscript_id] = book
        self.books_by_slug[book.slug] = book
        return book


class FakeNotificationRepository:
    def __init__(self, notifications=None):
        self.notifications = notifications or {}
        self.updated = []

    async def get_by_id_and_user_id(self, notification_id: str, user_id: int):
        notification = self.notifications.get(notification_id)
        if notification and notification.user_id == user_id:
            return notification
        return None

    async def update(self, notification: Notification):
        self.notifications[notification.id] = notification
        self.updated.append(notification)
        return notification

    async def list_by_user_id(self, user_id: int):
        return [n for n in self.notifications.values() if n.user_id == user_id]

    async def create(self, notification: Notification):
        notification.id = notification.id or "notif-1"
        self.notifications[notification.id] = notification
        return notification
