from datetime import datetime
from pydantic import BaseModel, Field


class CreateManuscriptRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    synopsis: str | None = Field(default=None, max_length=3000)


class UpdateManuscriptRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    synopsis: str | None = Field(default=None, max_length=3000)


class CreateChapterRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)


class UpdateChapterRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)


class ChapterResponse(BaseModel):
    id: str
    manuscript_id: str
    title: str
    content: str
    chapter_order: int


class ManuscriptResponse(BaseModel):
    id: str
    author_id: int
    title: str
    synopsis: str | None
    status: str
    created_at: datetime
    updated_at: datetime



class ManuscriptDetailsResponse(ManuscriptResponse):
    chapters: list[ChapterResponse]


class ManuscriptVersionResponse(BaseModel):
    id: str
    manuscript_id: str
    version_number: int
    title_snapshot: str
    synopsis_snapshot: str | None
    content_snapshot: str
    created_at: datetime
