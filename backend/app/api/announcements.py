from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.announcement import Announcement
from app.schemas.announcement import AnnouncementCreate, AnnouncementResponse

router = APIRouter(prefix="/api/announcements", tags=["Announcements"])


@router.get("/", response_model=list[AnnouncementResponse])
def list_announcements(
    category: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Announcement)
    if category:
        q = q.filter(Announcement.category == category)
    # Pinned first, then by date
    announcements = q.order_by(Announcement.pinned.desc(), Announcement.created_at.desc()).all()
    return [
        AnnouncementResponse(
            id=a.id,
            title=a.title,
            content=a.content,
            category=a.category,
            pinned=a.pinned,
            posted_by=a.posted_by,
            poster_name=a.poster.name if a.poster else None,
            created_at=a.created_at,
        )
        for a in announcements
    ]


@router.post("/", response_model=AnnouncementResponse)
def create_announcement(
    data: AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ("admin", "authority", "faculty"):
        raise HTTPException(403, "Not authorized to post announcements")
    a = Announcement(
        title=data.title,
        content=data.content,
        category=data.category,
        pinned=data.pinned,
        posted_by=current_user.id,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return AnnouncementResponse(
        id=a.id, title=a.title, content=a.content,
        category=a.category, pinned=a.pinned,
        posted_by=a.posted_by, poster_name=current_user.name,
        created_at=a.created_at,
    )


@router.delete("/{announcement_id}")
def delete_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    a = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not a:
        raise HTTPException(404, "Announcement not found")
    if a.posted_by != current_user.id and current_user.role != "admin":
        raise HTTPException(403, "Not authorized")
    db.delete(a)
    db.commit()
    return {"detail": "Deleted"}
