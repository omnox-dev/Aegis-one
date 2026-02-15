from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.incident import Incident

router = APIRouter(prefix="/api/emergency", tags=["Guardian's Flare"])

@router.post("/sos")
def trigger_sos(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = Incident(
        user_id=current_user.id,
        latitude=latitude,
        longitude=longitude,
        status="active"
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    
    # In a real app, this would trigger SMS/Push/Email to security
    return {
        "message": "Guardian's Flare activated. Help is on the way.",
        "incident_id": incident.id
    }

@router.get("/incidents", response_model=List[dict])
def list_incidents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ("admin", "authority"):
        raise HTTPException(status_code=403, detail="Not authorized to view medical/security incidents")
    
    incidents = db.query(Incident).order_by(Incident.created_at.desc()).all()
    return [
        {
            "id": i.id,
            "user": i.user.name,
            "status": i.status,
            "location": {"lat": i.latitude, "lng": i.longitude},
            "created_at": i.created_at
        } for i in incidents
    ]
