import pytest

from app.domain.entities.book_builder import BookBuilder, BookBuilderError


def test_book_builder_raises_without_required_fields():
    builder = BookBuilder()

    with pytest.raises(BookBuilderError):
        builder.build()


def test_book_builder_raises_if_slug_missing():
    builder = BookBuilder()
    builder._manuscript_id = "m1"
    builder._author_id = 4
    builder._title = "Titre"
    builder._content = "Contenu"
    builder._slug = None

    with pytest.raises(BookBuilderError):
        builder.build()
