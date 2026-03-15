from datetime import datetime
from pydantic import BaseModel, Field


class SubmitManuscriptRequest(BaseModel):
    note: str | None = Field(default=None, max_length=3000)


class EditorialActionRequest(BaseModel):
    note: str | None = Field(default=None, max_length=3000)


class EditorialDecisionRequest(BaseModel):
    note: str = Field(..., min_length=1, max_length=3000)


class EditorialDossierResponse(BaseModel):
    id: str
    manuscript_id: str
    submitted_by_user_id: int
    assigned_editor_id: int | None
    status: str
    submission_note: str | None
    editorial_note: str | None
    created_at: datetime
    updated_at: datetime
