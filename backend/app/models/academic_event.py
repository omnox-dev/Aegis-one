from datetime import datetime, timezone, date

from sqlalchemy import String, Text, DateTime, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AcademicEvent(Base):
    __tablename__ = "academic_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    event_type: Mapped[str] = mapped_column(String(30), default="deadline")  # exam, assignment, holiday, deadline, event
    course_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("courses.id"), nullable=True)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    creator = relationship("User", lazy="joined")
    course = relationship("Course", lazy="joined")
