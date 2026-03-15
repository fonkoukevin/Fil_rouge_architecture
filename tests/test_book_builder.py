from datetime import datetime, timezone

from app.domain.entities.book_builder import BookBuilder
from app.domain.entities.manuscript import Manuscript


def test_book_builder_builds_book_from_manuscript():
    manuscript = Manuscript(
        id="manu-1",
        author_id=4,
        title="Mon Roman de Test",
        synopsis="Une histoire",
        status="ACCEPTED",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        chapters=[],
    )

    book = BookBuilder().from_manuscript(manuscript).build()

    assert book.manuscript_id == "manu-1"
    assert book.author_id == 4
    assert book.title == "Mon Roman de Test"
    assert book.synopsis == "Une histoire"
    assert book.slug == "mon-roman-de-test"
    assert book.is_published is True
