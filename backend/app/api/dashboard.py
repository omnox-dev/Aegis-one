from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.grievance import Grievance
from app.models.course import Course, Enrollment
from app.models.internship import Internship, Application

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return role-aware dashboard statistics."""
    role = current_user.role

    if role == "student":
        total_grievances = db.query(Grievance).filter(Grievance.submitted_by == current_user.id).count()
        pending = db.query(Grievance).filter(Grievance.submitted_by == current_user.id, Grievance.status == "pending").count()
        in_review = db.query(Grievance).filter(Grievance.submitted_by == current_user.id, Grievance.status == "in_review").count()
        resolved = db.query(Grievance).filter(Grievance.submitted_by == current_user.id, Grievance.status == "resolved").count()
        enrolled_courses = db.query(Enrollment).filter(Enrollment.student_id == current_user.id).count()
        applied_internships = db.query(Application).filter(Application.student_id == current_user.id).count()

        return {
            "role": role,
            "stats": {
                "total_grievances": total_grievances,
                "pending": pending,
                "in_review": in_review,
                "resolved": resolved,
                "enrolled_courses": enrolled_courses,
                "applied_internships": applied_internships,
            },
        }

    elif role == "faculty":
        my_courses = db.query(Course).filter(Course.faculty_id == current_user.id).count()
        total_students = (
            db.query(Enrollment)
            .join(Course, Enrollment.course_id == Course.id)
            .filter(Course.faculty_id == current_user.id)
            .count()
        )
        my_internships = db.query(Internship).filter(Internship.posted_by == current_user.id).count()

        return {
            "role": role,
            "stats": {
                "my_courses": my_courses,
                "total_students": total_students,
                "posted_internships": my_internships,
            },
        }

    elif role == "authority":
        total = db.query(Grievance).count()
        pending = db.query(Grievance).filter(Grievance.status == "pending").count()
        in_review = db.query(Grievance).filter(Grievance.status == "in_review").count()
        resolved = db.query(Grievance).filter(Grievance.status == "resolved").count()
        rejected = db.query(Grievance).filter(Grievance.status == "rejected").count()
        assigned_to_me = db.query(Grievance).filter(Grievance.assigned_to == current_user.id).count()

        return {
            "role": role,
            "stats": {
                "total_grievances": total,
                "pending": pending,
                "in_review": in_review,
                "resolved": resolved,
                "rejected": rejected,
                "assigned_to_me": assigned_to_me,
            },
        }

    elif role == "admin":
        total_users = db.query(User).count()
        students = db.query(User).filter(User.role == "student").count()
        faculty = db.query(User).filter(User.role == "faculty").count()
        authorities = db.query(User).filter(User.role == "authority").count()
        total_grievances = db.query(Grievance).count()
        active_grievances = db.query(Grievance).filter(Grievance.status.in_(["pending", "in_review"])).count()
        total_courses = db.query(Course).count()
        total_internships = db.query(Internship).count()

        return {
            "role": role,
            "stats": {
                "total_users": total_users,
                "students": students,
                "faculty": faculty,
                "authorities": authorities,
                "total_grievances": total_grievances,
                "active_grievances": active_grievances,
                "total_courses": total_courses,
                "total_internships": total_internships,
            },
        }

    return {"role": role, "stats": {}}
