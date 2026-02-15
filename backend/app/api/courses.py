from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User
from app.models.course import Course, Enrollment
from app.schemas.course import CourseCreate, CourseResponse, EnrollmentCreate, EnrollmentResponse

router = APIRouter(prefix="/api/courses", tags=["Courses"])


@router.get("/", response_model=list[CourseResponse])
def list_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all courses with enrollment info."""
    courses = db.query(Course).order_by(Course.created_at.desc()).all()
    result = []
    for c in courses:
        enrollment_count = db.query(Enrollment).filter(Enrollment.course_id == c.id).count()
        is_enrolled = False
        if current_user.role == "student":
            is_enrolled = db.query(Enrollment).filter(
                Enrollment.course_id == c.id,
                Enrollment.student_id == current_user.id,
            ).first() is not None

        result.append(CourseResponse(
            id=c.id,
            name=c.name,
            code=c.code,
            description=c.description,
            semester=c.semester,
            credits=c.credits,
            course_type=c.course_type,
            faculty_id=c.faculty_id,
            faculty_name=c.faculty.name if c.faculty else None,
            created_at=c.created_at,
            enrollment_count=enrollment_count,
            is_enrolled=is_enrolled,
        ))
    return result


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("faculty", "admin")),
):
    """Create a new course (faculty/admin only)."""
    existing = db.query(Course).filter(Course.code == data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Course code already exists")

    course = Course(
        name=data.name,
        code=data.code,
        description=data.description,
        semester=data.semester,
        credits=data.credits,
        course_type=data.course_type,
        faculty_id=current_user.id,
    )
    db.add(course)
    db.commit()
    db.refresh(course)

    return CourseResponse(
        id=course.id,
        name=course.name,
        code=course.code,
        description=course.description,
        semester=course.semester,
        credits=course.credits,
        course_type=course.course_type,
        faculty_id=course.faculty_id,
        faculty_name=current_user.name,
        created_at=course.created_at,
    )


@router.post("/enroll", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_in_course(
    data: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("student")),
):
    """Enroll in a course (students only)."""
    course = db.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check if already enrolled
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id,
        Enrollment.course_id == data.course_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")

    enrollment = Enrollment(student_id=current_user.id, course_id=data.course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return EnrollmentResponse(
        id=enrollment.id,
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        course_name=course.name,
        course_code=course.code,
        credits=course.credits,
        course_type=course.course_type,
        enrolled_at=enrollment.enrolled_at,
    )


@router.get("/my-enrollments", response_model=list[EnrollmentResponse])
def my_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("student")),
):
    """Get current student's enrollments."""
    enrollments = db.query(Enrollment).filter(Enrollment.student_id == current_user.id).all()
    return [
        EnrollmentResponse(
            id=e.id,
            student_id=e.student_id,
            course_id=e.course_id,
            course_name=e.course.name if e.course else None,
            course_code=e.course.code if e.course else None,
            credits=e.course.credits if e.course else 0,
            course_type=e.course.course_type if e.course else "major",
            enrolled_at=e.enrolled_at,
        )
        for e in enrollments
    ]
