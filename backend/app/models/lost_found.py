from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class LostFoundItem(Base):
    __tablename__ = "lost_found_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category: Mapped[str] = mapped_column(String(30), default="other")  # electronics, books, id_cards, clothing, other
    item_type: Mapped[str] = mapped_column(String(10), default="found")  # lost, found
    status: Mapped[str] = mapped_column(String(20), default="open")  # open, claimed, closed
    posted_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    claimed_by: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    poster = relationship("User", foreign_keys=[posted_by], lazy="joined")
    claimer = relationship("User", foreign_keys=[claimed_by], lazy="joined")
