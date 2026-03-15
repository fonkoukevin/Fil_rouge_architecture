from app.domain.entities.chapter import Chapter


def test_chapter_creation():
    chapter = Chapter(
        id="c1",
        manuscript_id="m1",
        title="Chapitre 1",
        content="Contenu du chapitre",
        chapter_order=1,
    )

    assert chapter.title == "Chapitre 1"
    assert chapter.chapter_order == 1
    assert chapter.manuscript_id == "m1"
