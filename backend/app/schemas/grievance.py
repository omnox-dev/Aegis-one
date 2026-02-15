from datetime import datetime
from pydantic import BaseModel


class GrievanceCreate(BaseModel):
    title: str
    description: str
    category: str
    priority: str = "medium"
    location: str | None = None
    image_url: str | None = None
    is_anonymous: bool = False


class GrievanceUpdate(BaseModel):
    status: str | None = None
    assigned_to: int | None = None


class GrievanceCommentCreate(BaseModel):
    content: str


class GrievanceCommentResponse(BaseModel):
    id: int
    grievance_id: int
    user_id: int
    user_name: str | None = None
    user_role: str | None = None
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class GrievanceResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    priority: str
    status: str
    location: str | None = None
    image_url: str | None = None
    is_anonymous: bool = False
    submitted_by: int
    submitter_name: str | None = None
    assigned_to: int | None
    assignee_name: str | None = None
    created_at: datetime
    updated_at: datetime
    comments: list[GrievanceCommentResponse] = []

    model_config = {"from_attributes": True}
