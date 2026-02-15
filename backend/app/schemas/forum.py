from datetime import datetime
from pydantic import BaseModel


class ForumPostCreate(BaseModel):
    title: str
    content: str
    category: str = "general"
    image_url: str | None = None


class ForumCommentCreate(BaseModel):
    content: str
    parent_id: int | None = None


class ForumCommentResponse(BaseModel):
    id: int
    post_id: int
    parent_id: int | None
    author_id: int
    author_name: str | None = None
    content: str
    upvotes: int
    downvotes: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ForumPostResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    image_url: str | None = None
    author_id: int
    author_name: str | None = None
    upvotes: int
    downvotes: int
    comment_count: int = 0
    created_at: datetime
    comments: list[ForumCommentResponse] = []

    model_config = {"from_attributes": True}
