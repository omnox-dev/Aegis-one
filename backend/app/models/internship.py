from datetime import datetime, timezone, date

from sqlalchemy import String, Text, DateTime, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Internship(Base):
    __tablename__ = "internships"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str | None] = mapped_column(String(100), nullable=True)
    stipend: Mapped[int | None] = mapped_column(Integer, nullable=True)
    role_type: Mapped[str] = mapped_column(String(30), default="internship")  # internship, research, fulltime
    required_skills: Mapped[str | None] = mapped_column(Text, nullable=True)  # comma-separated
    duration: Mapped[str | None] = mapped_column(String(50), nullable=True)  # e.g. "3 months"
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    posted_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    poster = relationship("User", lazy="joined")


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    internship_id: Mapped[int] = mapped_column(Integer, ForeignKey("internships.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="submitted")  # submitted, under_review, shortlisted, accepted, rejected
    resume_url: Mapped[str | None] = mapped_column(String(500), nullable=True)  # Student resume link
    faculty_feedback: Mapped[str | None] = mapped_column(Text, nullable=True)  # Direct messaging/feedback
    applied_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    student = relationship("User", lazy="joined")
    internship = relationship("Internship", backref="applications", lazy="joined")
