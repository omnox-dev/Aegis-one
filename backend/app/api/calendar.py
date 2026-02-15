from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.academic_event import AcademicEvent
from app.schemas.academic_event import AcademicEventCreate, AcademicEventResponse

router = APIRouter(prefix="/api/calendar", tags=["Academic Calendar"])


@router.get("/events", response_model=list[AcademicEventResponse])
def list_events(
    event_type: str | None = None,
    course_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(AcademicEvent)
    if event_type:
        q = q.filter(AcademicEvent.event_type == event_type)
    if course_id:
        q = q.filter(AcademicEvent.course_id == course_id)
    events = q.order_by(AcademicEvent.event_date.asc()).all()
    return [
        AcademicEventResponse(
            id=e.id,
            title=e.title,
            description=e.description,
            event_date=e.event_date,
            event_type=e.event_type,
            course_id=e.course_id,
            course_name=e.course.name if e.course else None,
            created_by=e.created_by,
            creator_name=e.creator.name if e.creator else None,
            created_at=e.created_at,
        )
        for e in events
    ]


@router.post("/events", response_model=AcademicEventResponse)
def create_event(
    data: AcademicEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ("admin", "authority", "faculty"):
        raise HTTPException(403, "Only faculty/admin can create events")
    e = AcademicEvent(
        title=data.title,
        description=data.description,
        event_date=data.event_date,
        event_type=data.event_type,
        course_id=data.course_id,
        created_by=current_user.id,
    )
    db.add(e)
    db.commit()
    db.refresh(e)
    return AcademicEventResponse(
        id=e.id,
        title=e.title,
        description=e.description,
        event_date=e.event_date,
        event_type=e.event_type,
        course_id=e.course_id,
        course_name=e.course.name if e.course else None,
        created_by=e.created_by,
        creator_name=current_user.name,
        created_at=e.created_at,
    )


@router.delete("/events/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    e = db.query(AcademicEvent).filter(AcademicEvent.id == event_id).first()
    if not e:
        raise HTTPException(404, "Event not found")
    if e.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(403, "Not authorized")
    db.delete(e)
    db.commit()
    return {"detail": "Deleted"}
