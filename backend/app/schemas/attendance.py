from datetime import date, datetime
from pydantic import BaseModel


class AttendanceCreate(BaseModel):
    course_id: int
    date: date
    status: str = "present"  # present, absent, late


class AttendanceResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    course_name: str | None = None
    course_code: str | None = None
    date: date
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
