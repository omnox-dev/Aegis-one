from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CaravanPool(Base):
    __tablename__ = "caravan_pools"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    origin: Mapped[str] = mapped_column(String(255), default="IIT Mandi Campus")
    travel_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    available_seats: Mapped[int] = mapped_column(Integer, default=3)
    estimated_cost: Mapped[float | None] = mapped_column(Float, nullable=True) # For split-cost calculator
    contact_info: Mapped[str | None] = mapped_column(String(255), nullable=True) # Privacy controlled info
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="open") # open, full, completed
    posted_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    poster = relationship("User", foreign_keys=[posted_by], lazy="joined")


class MercenaryGig(Base):
    __tablename__ = "mercenary_gigs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False) # tutoring, design, coding, photography, other
    budget: Mapped[str | None] = mapped_column(String(100), nullable=True)
    required_skills: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="open") # open, assigned, completed
    posted_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True) # 1-5 stars for review system
    review_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    poster = relationship("User", foreign_keys=[posted_by], lazy="joined")
    worker = relationship("User", foreign_keys=[assigned_to], lazy="joined")
