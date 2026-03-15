from dataclasses import dataclass


@dataclass
class Chapter:
    id: str | None
    manuscript_id: str
    title: str
    content: str
    chapter_order: int

    def update(self, title: str, content: str) -> None:
        self.title = title.strip()
        self.content = content.strip()
