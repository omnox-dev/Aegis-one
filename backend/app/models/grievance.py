from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Grievance(Base):
    __tablename__ = "grievances"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # academic, infrastructure, hostel, food, administrative, financial, other
    priority: Mapped[str] = mapped_column(String(20), default="medium")  # low, medium, high, urgent
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, in_review, resolved, rejected
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)  # campus location tag
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)  # photo evidence link
    is_anonymous: Mapped[bool] = mapped_column(default=False)
    submitted_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    submitter = relationship("User", foreign_keys=[submitted_by], lazy="joined")
    assignee = relationship("User", foreign_keys=[assigned_to], lazy="joined")


class GrievanceComment(Base):
    __tablename__ = "grievance_comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    grievance_id: Mapped[int] = mapped_column(Integer, ForeignKey("grievances.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", lazy="joined")
    grievance = relationship("Grievance", backref="comments", lazy="joined")
