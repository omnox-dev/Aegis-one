from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    description: Mapped[str] = mapped_column(String(255), default="Emergency SOS Triggered")
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, investigating, resolved, false_alarm
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    resolution_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    user = relationship("User", lazy="joined")
