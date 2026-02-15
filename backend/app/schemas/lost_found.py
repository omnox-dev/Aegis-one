from datetime import datetime
from pydantic import BaseModel


class LostFoundCreate(BaseModel):
    title: str
    description: str | None = None
    image_url: str | None = None
    location: str | None = None
    category: str = "other"  # electronics, books, id_cards, clothing, other
    item_type: str = "found"  # lost, found


class LostFoundUpdate(BaseModel):
    status: str | None = None  # open, claimed, closed


class LostFoundResponse(BaseModel):
    id: int
    title: str
    description: str | None
    image_url: str | None
    location: str | None
    category: str
    item_type: str
    status: str
    posted_by: int
    poster_name: str | None = None
    claimed_by: int | None
    created_at: datetime

    model_config = {"from_attributes": True}
