from datetime import datetime
from pydantic import BaseModel


class AnnouncementCreate(BaseModel):
    title: str
    content: str
    category: str = "general"  # academic, events, administrative, emergency, general
    pinned: bool = False


class AnnouncementResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    pinned: bool
    posted_by: int
    poster_name: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
