from datetime import datetime
from pydantic import BaseModel


class CourseCreate(BaseModel):
    name: str
    code: str
    description: str | None = None
    semester: str | None = None
    credits: int = 3
    course_type: str = "major"  # major, minor, elective, lab, project


class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    description: str | None
    semester: str | None
    credits: int = 3
    course_type: str = "major"
    faculty_id: int
    faculty_name: str | None = None
    created_at: datetime
    enrollment_count: int = 0
    is_enrolled: bool = False

    model_config = {"from_attributes": True}


class EnrollmentCreate(BaseModel):
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    course_name: str | None = None
    course_code: str | None = None
    credits: int = 0
    course_type: str = "major"
    enrolled_at: datetime

    model_config = {"from_attributes": True}
