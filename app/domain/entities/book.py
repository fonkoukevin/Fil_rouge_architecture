from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Book:
    id: str | None
    manuscript_id: str
    author_id: int
    title: str
    synopsis: str | None
    content: str
    slug: str
    is_published: bool = True
    published_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
