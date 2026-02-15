from datetime import date, datetime
from pydantic import BaseModel


class AcademicEventCreate(BaseModel):
    title: str
    description: str | None = None
    event_date: date
    event_type: str = "deadline"  # exam, assignment, holiday, deadline, event
    course_id: int | None = None


class AcademicEventResponse(BaseModel):
    id: int
    title: str
    description: str | None
    event_date: date
    event_type: str
    course_id: int | None
    course_name: str | None = None
    created_by: int
    creator_name: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
