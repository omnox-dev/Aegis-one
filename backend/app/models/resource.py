from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_url: Mapped[str] = mapped_column(String(500), nullable=False)
    course_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    year: Mapped[str | None] = mapped_column(String(10), nullable=True)  # e.g. "2024"
    exam_type: Mapped[str | None] = mapped_column(String(30), nullable=True)  # midsem, endsem, quiz, notes
    resource_type: Mapped[str] = mapped_column(String(30), default="pyq")  # pyq, notes, assignment, other
    tags: Mapped[str | None] = mapped_column(Text, nullable=True)  # comma-separated
    uploaded_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    uploader = relationship("User", lazy="joined")
