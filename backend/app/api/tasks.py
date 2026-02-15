from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    category: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Task).filter(Task.user_id == current_user.id)
    if category:
        q = q.filter(Task.category == category)
    if status:
        q = q.filter(Task.status == status)
    return q.order_by(Task.created_at.desc()).all()


@router.post("/", response_model=TaskResponse)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    t = Task(
        title=data.title,
        description=data.description,
        due_date=data.due_date,
        category=data.category,
        priority=data.priority,
        user_id=current_user.id,
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    t = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not t:
        raise HTTPException(404, "Task not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(t, field, value)
    db.commit()
    db.refresh(t)
    return t


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    t = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not t:
        raise HTTPException(404, "Task not found")
    db.delete(t)
    db.commit()
    return {"detail": "Deleted"}
