from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.attendance import Attendance
from app.models.course import Enrollment
from app.schemas.attendance import AttendanceCreate, AttendanceResponse

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])


@router.get("/", response_model=list[AttendanceResponse])
def get_my_attendance(
    course_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Attendance).filter(Attendance.student_id == current_user.id)
    if course_id:
        q = q.filter(Attendance.course_id == course_id)
    records = q.order_by(Attendance.date.desc()).all()
    result = []
    for r in records:
        resp = AttendanceResponse(
            id=r.id,
            student_id=r.student_id,
            course_id=r.course_id,
            course_name=r.course.name if r.course else None,
            course_code=r.course.code if r.course else None,
            date=r.date,
            status=r.status,
            created_at=r.created_at,
        )
        result.append(resp)
    return result


@router.post("/", response_model=AttendanceResponse)
def mark_attendance(
    data: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "student":
        raise HTTPException(403, "Only students can mark attendance")
    # Check enrollment
    enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id,
        Enrollment.course_id == data.course_id
    ).first()
    if not enrollment:
        raise HTTPException(400, "You are not enrolled in this course")
    # Check if already marked
    existing = db.query(Attendance).filter(
        Attendance.student_id == current_user.id,
        Attendance.course_id == data.course_id,
        Attendance.date == data.date,
    ).first()
    if existing:
        existing.status = data.status
        db.commit()
        db.refresh(existing)
        rec = existing
    else:
        rec = Attendance(
            student_id=current_user.id,
            course_id=data.course_id,
            date=data.date,
            status=data.status,
        )
        db.add(rec)
        db.commit()
        db.refresh(rec)
    return AttendanceResponse(
        id=rec.id,
        student_id=rec.student_id,
        course_id=rec.course_id,
        course_name=rec.course.name if rec.course else None,
        course_code=rec.course.code if rec.course else None,
        date=rec.date,
        status=rec.status,
        created_at=rec.created_at,
    )


@router.get("/summary")
def attendance_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get attendance percentage per enrolled course."""
    enrollments = db.query(Enrollment).filter(Enrollment.student_id == current_user.id).all()
    summary = []
    for e in enrollments:
        total = db.query(Attendance).filter(
            Attendance.student_id == current_user.id,
            Attendance.course_id == e.course_id,
        ).count()
        present = db.query(Attendance).filter(
            Attendance.student_id == current_user.id,
            Attendance.course_id == e.course_id,
            Attendance.status == "present",
        ).count()
        summary.append({
            "course_id": e.course_id,
            "course_name": e.course.name if e.course else None,
            "course_code": e.course.code if e.course else None,
            "total_classes": total,
            "present": present,
            "percentage": round(present / total * 100, 1) if total > 0 else 0,
        })
    return summary
