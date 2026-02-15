from datetime import datetime
from pydantic import BaseModel


class ResourceCreate(BaseModel):
    title: str
    description: str | None = None
    file_url: str
    course_code: str | None = None
    year: str | None = None
    exam_type: str | None = None
    resource_type: str = "pyq"
    tags: str | None = None


class ResourceResponse(BaseModel):
    id: int
    title: str
    description: str | None
    file_url: str
    course_code: str | None
    year: str | None
    exam_type: str | None
    resource_type: str
    tags: str | None
    uploaded_by: int
    uploader_name: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
