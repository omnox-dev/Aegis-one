from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.core.database import get_db
from app.core.deps import require_role
from app.models.location import CampusLocation
from app.models.user import User

class LocationCreate(BaseModel):
    name: str
    description: str
    category: str
    latitude: float
    longitude: float

router = APIRouter(prefix="/api/map", tags=["Pathfinder's Map"])

@router.post("/locations", status_code=201)
def create_location(
    data: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    loc = CampusLocation(
        name=data.name,
        description=data.description,
        category=data.category,
        latitude=data.latitude,
        longitude=data.longitude
    )
    db.add(loc)
    db.commit()
    db.refresh(loc)
    return loc

@router.delete("/locations/{loc_id}")
def delete_location(
    loc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    loc = db.query(CampusLocation).filter(CampusLocation.id == loc_id).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(loc)
    db.commit()
    return {"message": "Location deleted"}

@router.get("/locations", response_model=List[dict])
def get_locations(db: Session = Depends(get_db)):
    locations = db.query(CampusLocation).all()
    return [
        {
            "id": l.id,
            "name": l.name,
            "description": l.description,
            "category": l.category,
            "lat": l.latitude,
            "lng": l.longitude
        } for l in locations
    ]

@router.get("/search")
def search_locations(q: str, db: Session = Depends(get_db)):
    locations = db.query(CampusLocation).filter(CampusLocation.name.ilike(f"%{q}%")).all()
    return locations
