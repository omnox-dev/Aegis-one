from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import csv
import io

from app.core.database import get_db
from app.core.deps import require_role
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserCreate

router = APIRouter(prefix="/api/users", tags=["User Management"])


@router.get("/", response_model=list[UserResponse])
def list_users(
    role: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    """List all users (admin only)."""
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if status:
        query = query.filter(User.status == status)
    users = query.order_by(User.created_at.desc()).all()
    return [UserResponse.model_validate(u) for u in users]


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    """Create a user manually (admin only)."""
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        email=data.email,
        name=data.name,
        hashed_password=hash_password(data.password),
        role=data.role,
        department=data.department,
        status="active"  # Admin-created users are active by default
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    """Update a user's info/role (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.name is not None:
        user.name = data.name
    if data.department is not None:
        user.department = data.department
    if data.role is not None:
        valid_roles = {"student", "faculty", "authority", "admin"}
        if data.role not in valid_roles:
            raise HTTPException(status_code=400, detail=f"Invalid role. Must be one of: {valid_roles}")
        user.role = data.role
    
    if data.status is not None:
        valid_statuses = {"pending", "active", "rejected"}
        if data.status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
        user.status = data.status
    
    if data.managed_modules is not None:
        user.managed_modules = data.managed_modules

    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    """Delete a user (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    db.delete(user)
    db.commit()


@router.post("/bulk-import", status_code=status.HTTP_201_CREATED)
def bulk_import_users(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    """Bulk import users from CSV (admin only)."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        content = file.file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))
        
        imported_count = 0
        errors = []
        
        for row in reader:
            email = row.get("email", "").strip().lower()
            name = row.get("name", "").strip()
            role = row.get("role", "student").strip().lower()
            dept = row.get("department", "").strip()

            if not email or not name:
                errors.append(f"Skipped row with missing email/name: {row}")
                continue

            # Check if user exists
            existing = db.query(User).filter(User.email == email).first()
            if existing:
                errors.append(f"User {email} already exists")
                continue

            # Create user
            default_password = hash_password("Aegis@123")
            new_user = User(
                email=email,
                name=name,
                role=role if role in {"student", "faculty", "authority", "admin"} else "student",
                department=dept if dept else None,
                hashed_password=default_password,
                status="active"  # Admin imports are active by default
            )
            db.add(new_user)
            imported_count += 1

        db.commit()
        return {
            "message": f"Successfully imported {imported_count} users",
            "skipped": errors
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")
