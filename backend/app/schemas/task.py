from datetime import date, datetime
from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    due_date: date | None = None
    category: str = "assignment"  # assignment, project, personal, exam_prep
    priority: str = "medium"  # low, medium, high


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: date | None = None
    category: str | None = None
    status: str | None = None  # todo, in_progress, done
    priority: str | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    due_date: date | None
    category: str
    status: str
    priority: str
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
