from dataclasses import dataclass
from datetime import datetime


@dataclass
class ManuscriptVersion:
    id: str | None
    manuscript_id: str
    version_number: int
    title_snapshot: str
    synopsis_snapshot: str | None
    content_snapshot: str
    created_at: datetime
