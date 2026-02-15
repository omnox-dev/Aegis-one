from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User
from app.models.grievance import Grievance, GrievanceComment
from app.schemas.grievance import (
    GrievanceCreate,
    GrievanceUpdate,
    GrievanceResponse,
    GrievanceCommentCreate,
    GrievanceCommentResponse,
)

router = APIRouter(prefix="/api/grievances", tags=["Grievances"])


def _to_response(g: Grievance) -> GrievanceResponse:
    """Convert Grievance ORM object to response schema."""
    comments_data = []
    for c in (g.comments or []):
        comments_data.append(GrievanceCommentResponse(
            id=c.id,
            grievance_id=c.grievance_id,
            user_id=c.user_id,
            user_name=c.user.name if c.user else None,
            user_role=c.user.role if c.user else None,
            content=c.content,
            created_at=c.created_at,
        ))

    return GrievanceResponse(
        id=g.id,
        title=g.title,
        description=g.description,
        category=g.category,
        priority=g.priority,
        status=g.status,
        location=g.location,
        image_url=g.image_url,
        is_anonymous=g.is_anonymous,
        submitted_by=g.submitted_by,
        submitter_name="Anonymous" if g.is_anonymous else (g.submitter.name if g.submitter else None),
        assigned_to=g.assigned_to,
        assignee_name=g.assignee.name if g.assignee else None,
        created_at=g.created_at,
        updated_at=g.updated_at,
        comments=comments_data,
    )


@router.get("/", response_model=list[GrievanceResponse])
def list_grievances(
    status_filter: str | None = Query(None, alias="status"),
    category: str | None = None,
    priority: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List grievances. Students see their own; authority/admin see all."""
    query = db.query(Grievance)

    # Students only see their own grievances
    if current_user.role == "student":
        query = query.filter(Grievance.submitted_by == current_user.id)
    elif current_user.role == "authority":
        # Authority sees assigned + unassigned grievances
        query = query.filter(
            (Grievance.assigned_to == current_user.id) | (Grievance.assigned_to.is_(None))
        )
    # Admin and faculty see all

    if status_filter:
        query = query.filter(Grievance.status == status_filter)
    if category:
        query = query.filter(Grievance.category == category)
    if priority:
        query = query.filter(Grievance.priority == priority)

    grievances = query.order_by(Grievance.created_at.desc()).all()
    return [_to_response(g) for g in grievances]


@router.post("/", response_model=GrievanceResponse, status_code=status.HTTP_201_CREATED)
def create_grievance(
    data: GrievanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit a new grievance (any authenticated user, typically students)."""
    grievance = Grievance(
        title=data.title,
        description=data.description,
        category=data.category,
        priority=data.priority,
        location=data.location,
        image_url=data.image_url,
        is_anonymous=data.is_anonymous,
        submitted_by=current_user.id,
    )
    db.add(grievance)
    db.commit()
    db.refresh(grievance)
    return _to_response(grievance)


@router.get("/{grievance_id}", response_model=GrievanceResponse)
def get_grievance(
    grievance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single grievance by ID."""
    grievance = db.query(Grievance).filter(Grievance.id == grievance_id).first()
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")

    # Students can only view their own
    if current_user.role == "student" and grievance.submitted_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return _to_response(grievance)


@router.patch("/{grievance_id}", response_model=GrievanceResponse)
def update_grievance(
    grievance_id: int,
    data: GrievanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("authority", "admin")),
):
    """Update grievance status or assignment (authority/admin only)."""
    grievance = db.query(Grievance).filter(Grievance.id == grievance_id).first()
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")

    if data.status is not None:
        valid_statuses = {"pending", "in_review", "in_progress", "resolved", "rejected"}
        if data.status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
        grievance.status = data.status

    if data.assigned_to is not None:
        # Verify the assignee exists and is authority/admin
        assignee = db.query(User).filter(User.id == data.assigned_to).first()
        if not assignee:
            raise HTTPException(status_code=404, detail="Assignee not found")
        grievance.assigned_to = data.assigned_to

    db.commit()
    db.refresh(grievance)
    return _to_response(grievance)


@router.delete("/{grievance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grievance(
    grievance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    """Delete a grievance (admin only)."""
    grievance = db.query(Grievance).filter(Grievance.id == grievance_id).first()
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")
    db.delete(grievance)
    db.commit()


# --- Comments (Timeline) ---

@router.post("/{grievance_id}/comments", response_model=GrievanceCommentResponse, status_code=status.HTTP_201_CREATED)
def add_comment(
    grievance_id: int,
    data: GrievanceCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a comment to a grievance (for timeline/audit log)."""
    grievance = db.query(Grievance).filter(Grievance.id == grievance_id).first()
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")

    comment = GrievanceComment(
        grievance_id=grievance_id,
        user_id=current_user.id,
        content=data.content,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return GrievanceCommentResponse(
        id=comment.id,
        grievance_id=comment.grievance_id,
        user_id=comment.user_id,
        user_name=current_user.name,
        user_role=current_user.role,
        content=comment.content,
        created_at=comment.created_at,
    )
