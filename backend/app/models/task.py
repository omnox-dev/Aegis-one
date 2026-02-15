from datetime import datetime, timezone, date

from sqlalchemy import String, Text, DateTime, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    category: Mapped[str] = mapped_column(String(30), default="assignment")  # assignment, project, personal, exam_prep
    status: Mapped[str] = mapped_column(String(20), default="todo")  # todo, in_progress, done
    priority: Mapped[str] = mapped_column(String(20), default="medium")  # low, medium, high
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", lazy="joined")
