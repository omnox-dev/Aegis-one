from __future__ import annotations
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ForumComment(Base):
    __tablename__ = "forum_comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("forum_posts.id"), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("forum_comments.id"), nullable=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    upvotes: Mapped[int] = mapped_column(Integer, default=0)
    downvotes: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    author: Mapped["User"] = relationship("User", lazy="joined")
    post: Mapped["ForumPost"] = relationship("ForumPost", back_populates="comments")


class ForumPost(Base):
    __tablename__ = "forum_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(30), default="general")  # academics, campus_life, events, tech_support, general
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    upvotes: Mapped[int] = mapped_column(Integer, default=0)
    downvotes: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    author: Mapped["User"] = relationship("User", lazy="joined")
    comments: Mapped[list["ForumComment"]] = relationship("ForumComment", back_populates="post", lazy="selectin", cascade="all, delete-orphan")
