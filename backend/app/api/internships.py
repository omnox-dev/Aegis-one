from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User
from app.models.internship import Internship, Application
from app.schemas.internship import (
    InternshipCreate,
    InternshipResponse,
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
)

router = APIRouter(prefix="/api/internships", tags=["Internships"])


@router.get("/", response_model=list[InternshipResponse])
def list_internships(
    role_type: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all internships with application info."""
    query = db.query(Internship)
    if role_type:
        query = query.filter(Internship.role_type == role_type)

    internships = query.order_by(Internship.created_at.desc()).all()
    result = []
    for i in internships:
        app_count = db.query(Application).filter(Application.internship_id == i.id).count()
        has_applied = False
        if current_user.role == "student":
            has_applied = db.query(Application).filter(
                Application.internship_id == i.id,
                Application.student_id == current_user.id,
            ).first() is not None

        result.append(InternshipResponse(
            id=i.id,
            title=i.title,
            company=i.company,
            description=i.description,
            location=i.location,
            stipend=i.stipend,
            role_type=i.role_type,
            required_skills=i.required_skills,
            duration=i.duration,
            deadline=i.deadline,
            posted_by=i.posted_by,
            poster_name=i.poster.name if i.poster else None,
            created_at=i.created_at,
            application_count=app_count,
            has_applied=has_applied,
        ))
    return result


@router.post("/", response_model=InternshipResponse, status_code=status.HTTP_201_CREATED)
def create_internship(
    data: InternshipCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("faculty", "admin")),
):
    """Post a new internship (faculty/admin only)."""
    internship = Internship(
        title=data.title,
        company=data.company,
        description=data.description,
        location=data.location,
        stipend=data.stipend,
        role_type=data.role_type,
        required_skills=data.required_skills,
        duration=data.duration,
        deadline=data.deadline,
        posted_by=current_user.id,
    )
    db.add(internship)
    db.commit()
    db.refresh(internship)

    return InternshipResponse(
        id=internship.id,
        title=internship.title,
        company=internship.company,
        description=internship.description,
        location=internship.location,
        stipend=internship.stipend,
        role_type=internship.role_type,
        required_skills=internship.required_skills,
        duration=internship.duration,
        deadline=internship.deadline,
        posted_by=internship.posted_by,
        poster_name=current_user.name,
        created_at=internship.created_at,
    )


@router.post("/apply", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def apply_to_internship(
    data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("student")),
):
    """Apply to an internship (students only)."""
    internship = db.query(Internship).filter(Internship.id == data.internship_id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")

    existing = db.query(Application).filter(
        Application.student_id == current_user.id,
        Application.internship_id == data.internship_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this internship")

    application = Application(student_id=current_user.id, internship_id=data.internship_id)
    db.add(application)
    db.commit()
    db.refresh(application)

    return ApplicationResponse(
        id=application.id,
        student_id=application.student_id,
        student_name=current_user.name,
        internship_id=application.internship_id,
        internship_title=internship.title,
        company=internship.company,
        status=application.status,
        applied_at=application.applied_at,
    )


@router.get("/my-applications", response_model=list[ApplicationResponse])
def my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("student")),
):
    """Get current student's internship applications."""
    applications = db.query(Application).filter(Application.student_id == current_user.id).all()
    return [
        ApplicationResponse(
            id=a.id,
            student_id=a.student_id,
            student_name=current_user.name,
            internship_id=a.internship_id,
            internship_title=a.internship.title if a.internship else None,
            company=a.internship.company if a.internship else None,
            status=a.status,
            faculty_feedback=a.faculty_feedback,
            applied_at=a.applied_at,
        )
        for a in applications
    ]


# --- Faculty Application Management ---

@router.get("/{internship_id}/applications", response_model=list[ApplicationResponse])
def list_applications(
    internship_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("faculty", "admin")),
):
    """View applications for a specific internship (faculty/admin only)."""
    internship = db.query(Internship).filter(Internship.id == internship_id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
    if internship.posted_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    applications = db.query(Application).filter(Application.internship_id == internship_id).all()
    return [
        ApplicationResponse(
            id=a.id,
            student_id=a.student_id,
            student_name=a.student.name if a.student else None,
            internship_id=a.internship_id,
            internship_title=internship.title,
            company=internship.company,
            status=a.status,
            faculty_feedback=a.faculty_feedback,
            applied_at=a.applied_at,
        )
        for a in applications
    ]


@router.patch("/{internship_id}/applications/{application_id}", response_model=ApplicationResponse)
def update_application_status(
    internship_id: int,
    application_id: int,
    data: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("faculty", "admin")),
):
    """Update application status — accept, reject, shortlist, and add feedback (faculty/admin only)."""
    internship = db.query(Internship).filter(Internship.id == internship_id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
    if internship.posted_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    application = db.query(Application).filter(
        Application.id == application_id,
        Application.internship_id == internship_id,
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    valid_statuses = {"submitted", "under_review", "shortlisted", "accepted", "rejected"}
    if data.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")

    application.status = data.status
    if data.faculty_feedback is not None:
        application.faculty_feedback = data.faculty_feedback
    
    db.commit()
    db.refresh(application)

    return ApplicationResponse(
        id=application.id,
        student_id=application.student_id,
        student_name=application.student.name if application.student else None,
        internship_id=application.internship_id,
        internship_title=internship.title,
        company=internship.company,
        status=application.status,
        faculty_feedback=application.faculty_feedback,
        applied_at=application.applied_at,
    )
