from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.lost_found import LostFoundItem
from app.schemas.lost_found import LostFoundCreate, LostFoundUpdate, LostFoundResponse

router = APIRouter(prefix="/api/lost-found", tags=["Lost & Found"])


@router.get("/", response_model=list[LostFoundResponse])
def list_items(
    category: str | None = None,
    item_type: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(LostFoundItem)
    if category:
        q = q.filter(LostFoundItem.category == category)
    if item_type:
        q = q.filter(LostFoundItem.item_type == item_type)
    if status:
        q = q.filter(LostFoundItem.status == status)
    items = q.order_by(LostFoundItem.created_at.desc()).all()
    return [
        LostFoundResponse(
            id=i.id,
            title=i.title,
            description=i.description,
            image_url=i.image_url,
            location=i.location,
            category=i.category,
            item_type=i.item_type,
            status=i.status,
            posted_by=i.posted_by,
            poster_name=i.poster.name if i.poster else None,
            claimed_by=i.claimed_by,
            created_at=i.created_at,
        )
        for i in items
    ]


@router.post("/", response_model=LostFoundResponse)
def create_item(
    data: LostFoundCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    i = LostFoundItem(
        title=data.title,
        description=data.description,
        image_url=data.image_url,
        location=data.location,
        category=data.category,
        item_type=data.item_type,
        posted_by=current_user.id,
    )
    db.add(i)
    db.commit()
    db.refresh(i)
    return LostFoundResponse(
        id=i.id, title=i.title, description=i.description,
        image_url=i.image_url, location=i.location,
        category=i.category, item_type=i.item_type,
        status=i.status, posted_by=i.posted_by,
        poster_name=current_user.name, claimed_by=i.claimed_by,
        created_at=i.created_at,
    )


@router.patch("/{item_id}/claim", response_model=LostFoundResponse)
def claim_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    i = db.query(LostFoundItem).filter(LostFoundItem.id == item_id).first()
    if not i:
        raise HTTPException(404, "Item not found")
    if i.status != "open":
        raise HTTPException(400, "Item already claimed or closed")
    i.claimed_by = current_user.id
    i.status = "claimed"
    db.commit()
    db.refresh(i)
    return LostFoundResponse(
        id=i.id, title=i.title, description=i.description,
        image_url=i.image_url, location=i.location,
        category=i.category, item_type=i.item_type,
        status=i.status, posted_by=i.posted_by,
        poster_name=i.poster.name if i.poster else None,
        claimed_by=i.claimed_by, created_at=i.created_at,
    )


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    i = db.query(LostFoundItem).filter(LostFoundItem.id == item_id).first()
    if not i:
        raise HTTPException(404, "Item not found")
    if i.posted_by != current_user.id and current_user.role not in ("admin",):
        raise HTTPException(403, "Not authorized")
    db.delete(i)
    db.commit()
    return {"detail": "Deleted"}
