from datetime import datetime, date
from pydantic import BaseModel


class InternshipCreate(BaseModel):
    title: str
    company: str
    description: str | None = None
    location: str | None = None
    stipend: int | None = None
    role_type: str = "internship"
    required_skills: str | None = None
    duration: str | None = None
    deadline: date | None = None


class InternshipResponse(BaseModel):
    id: int
    title: str
    company: str
    description: str | None
    location: str | None
    stipend: int | None
    role_type: str
    required_skills: str | None = None
    duration: str | None = None
    deadline: date | None
    posted_by: int
    poster_name: str | None = None
    created_at: datetime
    application_count: int = 0
    has_applied: bool = False

    model_config = {"from_attributes": True}


class ApplicationCreate(BaseModel):
    internship_id: int


class ApplicationUpdate(BaseModel):
    status: str  # submitted, under_review, shortlisted, accepted, rejected
    faculty_feedback: str | None = None


class ApplicationResponse(BaseModel):
    id: int
    student_id: int
    student_name: str | None = None
    internship_id: int
    internship_title: str | None = None
    company: str | None = None
    status: str
    faculty_feedback: str | None = None
    applied_at: datetime

    model_config = {"from_attributes": True}
