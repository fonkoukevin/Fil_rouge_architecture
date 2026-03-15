from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.entities.chapter import Chapter
from app.domain.services.manuscript_state import get_state


class ManuscriptError(Exception):
    pass


@dataclass
class Manuscript:
    id: str | None
    author_id: int
    title: str
    synopsis: str | None
    status: str = "DRAFT"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    chapters: list[Chapter] = field(default_factory=list)

    def update_metadata(self, title: str, synopsis: str | None) -> None:
        state = get_state(self.status)
        if not state.can_edit():
            raise ManuscriptError("Ce manuscrit ne peut plus être modifié dans son état actuel.")

        self.title = title.strip()
        self.synopsis = synopsis.strip() if synopsis else None
        self.updated_at = datetime.now(timezone.utc)

    def add_chapter(self, chapter: Chapter) -> None:
        state = get_state(self.status)
        if not state.can_edit():
            raise ManuscriptError("Impossible d'ajouter un chapitre à ce manuscrit.")

        self.chapters.append(chapter)
        self.updated_at = datetime.now(timezone.utc)

    def submit(self) -> None:
        state = get_state(self.status)
        self.status = state.submit()
        self.updated_at = datetime.now(timezone.utc)

    def build_snapshot_content(self) -> str:
        ordered_chapters = sorted(self.chapters, key=lambda chapter: chapter.chapter_order)
        return "\n\n".join(
            f"# {chapter.title}\n{chapter.content}" for chapter in ordered_chapters
        )
