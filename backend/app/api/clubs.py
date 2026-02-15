from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User
from app.models.clubs import Club, ClubMember, ClubEvent, ClubAnnouncement
from pydantic import BaseModel

class ClubCreate(BaseModel):
    name: str
    description: str
    category: str
    lead_id: int
    logo_url: str | None = None

router = APIRouter(prefix="/api/clubs", tags=["The Spirit - Clubs"])

@router.post("/", status_code=201)
def create_club(
    data: ClubCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    club = Club(
        name=data.name,
        description=data.description,
        category=data.category,
        logo_url=data.logo_url,
        lead_id=data.lead_id
    )
    db.add(club)
    db.commit()
    db.refresh(club)
    return club

@router.delete("/{club_id}")
def delete_club(
    club_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    db.delete(club)
    db.commit()
    return {"message": "Club deleted"}

@router.get("/", response_model=List[dict])
def list_clubs(db: Session = Depends(get_db)):
    clubs = db.query(Club).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "category": c.category,
            "logo_url": c.logo_url,
            "member_count": len(c.members),
            "lead": c.lead.name if c.lead else "Unknown"
        } for c in clubs
    ]

@router.post("/{club_id}/join")
def join_club(
    club_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if already a member
    existing = db.query(ClubMember).filter(ClubMember.club_id == club_id, ClubMember.user_id == current_user.id).first()
    if existing:
        return {"message": "Already a member"}
    
    member = ClubMember(club_id=club_id, user_id=current_user.id)
    db.add(member)
    db.commit()
    return {"message": "Joined club successfully"}

@router.get("/{club_id}", response_model=dict)
def get_club_detail(club_id: int, db: Session = Depends(get_db)):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    
    events = db.query(ClubEvent).filter(ClubEvent.club_id == club_id).order_by(ClubEvent.event_date.asc()).all()
    announcements = db.query(ClubAnnouncement).filter(ClubAnnouncement.club_id == club_id).order_by(ClubAnnouncement.created_at.desc()).all()
    
    return {
        "id": club.id,
        "name": club.name,
        "description": club.description,
        "category": club.category,
        "logo_url": club.logo_url,
        "lead": club.lead.name if club.lead else "Unknown",
        "member_count": len(club.members),
        "events": [
            {
                "id": e.id,
                "title": e.title,
                "description": e.description,
                "date": e.event_date.isoformat(),
                "location": e.location
            } for e in events
        ],
        "announcements": [
            {
                "id": a.id,
                "title": a.title,
                "content": a.content,
                "date": a.created_at.isoformat()
            } for a in announcements
        ]
    }
