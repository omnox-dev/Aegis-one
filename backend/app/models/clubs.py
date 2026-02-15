from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Club(Base):
    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="technical") # technical, cultural, sports, social
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    lead = relationship("User", lazy="joined")
    members = relationship("ClubMember", back_populates="club", lazy="selectin")


class ClubMember(Base):
    __tablename__ = "club_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    club_id: Mapped[int] = mapped_column(Integer, ForeignKey("clubs.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(30), default="member") # member, coordinator, core
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    club = relationship("Club", back_populates="members")
    user = relationship("User", lazy="joined")


class ClubEvent(Base):
    __tablename__ = "club_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    club_id: Mapped[int] = mapped_column(Integer, ForeignKey("clubs.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    event_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class ClubAnnouncement(Base):
    __tablename__ = "club_announcements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    club_id: Mapped[int] = mapped_column(Integer, ForeignKey("clubs.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
