from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="student")  # student, faculty, authority, admin
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")  # pending, active, rejected
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    managed_modules: Mapped[str | None] = mapped_column(String(500), nullable=True) # Comma-separated list of modules
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
