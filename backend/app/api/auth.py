from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    from app.core.config import settings
    
    # Check if email domain is official
    if not data.email.endswith(f"@{settings.OFFICIAL_EMAIL_DOMAIN}"):
        raise HTTPException(
            status_code=400, 
            detail=f"Registration restricted to @{settings.OFFICIAL_EMAIL_DOMAIN} emails"
        )

    # Check if email already exists
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validate role
    valid_roles = {"student", "faculty", "authority", "admin"}
    if data.role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Invalid role. Must be one of: {valid_roles}")

    # Create user with pending status
    user = User(
        email=data.email,
        name=data.name,
        hashed_password=hash_password(data.password),
        role=data.role,
        department=data.department,
        status="pending"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password."""
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if user.status == "pending":
        raise HTTPException(
            status_code=403, 
            detail="Your account is pending admin approval. Please check back later."
        )
    
    if user.status == "rejected":
        raise HTTPException(
            status_code=403, 
            detail="Your registration request was rejected. Contact admin for details."
        )

    token = create_access_token({"sub": str(user.id), "role": user.role})

    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get the current authenticated user."""
    return UserResponse.model_validate(current_user)
