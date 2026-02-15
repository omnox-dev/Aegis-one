from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.caravan_mercenary import CaravanPool, MercenaryGig

router = APIRouter(prefix="/api/commons", tags=["The Commons"])

# --- Caravan Pool (Ride Sharing) ---

@router.get("/caravan", response_model=List[dict])
def list_caravans(db: Session = Depends(get_db)):
    caravans = db.query(CaravanPool).all()
    return [
        {
            "id": c.id,
            "destination": c.destination,
            "origin": c.origin,
            "travel_date": c.travel_date.isoformat(),
            "available_seats": c.available_seats,
            "estimated_cost": c.estimated_cost,
            "posted_by": c.poster.name,
            "status": c.status
        } for c in caravans
    ]

@router.post("/caravan")
def create_caravan(
    destination: str,
    travel_date: datetime,
    seats: int = 3,
    cost: float = 0.0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    caravan = CaravanPool(
        destination=destination,
        travel_date=travel_date,
        available_seats=seats,
        estimated_cost=cost,
        posted_by=current_user.id
    )
    db.add(caravan)
    db.commit()
    return {"message": "Ride share posted successfully"}

# --- Mercenary Guild (Freelancing) ---

@router.get("/mercenary", response_model=List[dict])
def list_gigs(db: Session = Depends(get_db)):
    gigs = db.query(MercenaryGig).all()
    return [
        {
            "id": g.id,
            "title": g.title,
            "category": g.category,
            "budget": g.budget,
            "status": g.status,
            "posted_by": g.poster.name
        } for g in gigs
    ]

@router.post("/mercenary")
def create_gig(
    title: str,
    description: str,
    category: str,
    budget: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    gig = MercenaryGig(
        title=title,
        description=description,
        category=category,
        budget=budget,
        posted_by=current_user.id
    )
    db.add(gig)
    db.commit()
    return {"message": "Mercenary gig posted successfully"}
