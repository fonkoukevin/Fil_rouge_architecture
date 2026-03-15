from datetime import datetime
from pydantic import BaseModel, Field


class PublishManuscriptRequest(BaseModel):
    manuscript_id: str = Field(..., min_length=1)


class BookResponse(BaseModel):
    id: str
    manuscript_id: str
    author_id: int
    title: str
    synopsis: str | None
    content: str
    slug: str
    is_published: bool
    published_at: datetime
    created_at: datetime
