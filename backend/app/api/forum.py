from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.forum import ForumPost, ForumComment
from app.schemas.forum import (
    ForumPostCreate, ForumPostResponse,
    ForumCommentCreate, ForumCommentResponse,
)

router = APIRouter(prefix="/api/forum", tags=["Forum"])


@router.get("/posts", response_model=list[ForumPostResponse])
def list_posts(
    category: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(ForumPost)
    if category:
        q = q.filter(ForumPost.category == category)
    posts = q.order_by(ForumPost.created_at.desc()).all()
    result = []
    for p in posts:
        comment_count = db.query(ForumComment).filter(ForumComment.post_id == p.id).count()
        result.append(ForumPostResponse(
            id=p.id,
            title=p.title,
            content=p.content,
            category=p.category,
            image_url=p.image_url,
            author_id=p.author_id,
            author_name=p.author.name if p.author else None,
            upvotes=p.upvotes,
            downvotes=p.downvotes,
            comment_count=comment_count,
            created_at=p.created_at,
        ))
    return result


@router.get("/posts/{post_id}", response_model=ForumPostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    p = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not p:
        raise HTTPException(404, "Post not found")
    comments = db.query(ForumComment).filter(ForumComment.post_id == post_id).order_by(ForumComment.created_at.asc()).all()
    comment_list = [
        ForumCommentResponse(
            id=c.id, post_id=c.post_id, parent_id=c.parent_id,
            author_id=c.author_id, author_name=c.author.name if c.author else None,
            content=c.content, upvotes=c.upvotes, downvotes=c.downvotes,
            created_at=c.created_at,
        )
        for c in comments
    ]
    return ForumPostResponse(
        id=p.id, title=p.title, content=p.content,
        category=p.category, image_url=p.image_url,
        author_id=p.author_id,
        author_name=p.author.name if p.author else None,
        upvotes=p.upvotes, downvotes=p.downvotes,
        comment_count=len(comment_list),
        created_at=p.created_at, comments=comment_list,
    )


@router.post("/posts", response_model=ForumPostResponse)
def create_post(
    data: ForumPostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    p = ForumPost(
        title=data.title,
        content=data.content,
        category=data.category,
        image_url=data.image_url,
        author_id=current_user.id,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return ForumPostResponse(
        id=p.id, title=p.title, content=p.content,
        category=p.category, image_url=p.image_url,
        author_id=p.author_id,
        author_name=current_user.name,
        upvotes=0, downvotes=0, comment_count=0,
        created_at=p.created_at,
    )


@router.post("/posts/{post_id}/comments", response_model=ForumCommentResponse)
def add_comment(
    post_id: int,
    data: ForumCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    c = ForumComment(
        post_id=post_id,
        parent_id=data.parent_id,
        author_id=current_user.id,
        content=data.content,
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return ForumCommentResponse(
        id=c.id, post_id=c.post_id, parent_id=c.parent_id,
        author_id=c.author_id, author_name=current_user.name,
        content=c.content, upvotes=0, downvotes=0,
        created_at=c.created_at,
    )


@router.post("/posts/{post_id}/vote")
def vote_post(
    post_id: int,
    vote: str,  # "up" or "down"
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    p = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not p:
        raise HTTPException(404, "Post not found")
    if vote == "up":
        p.upvotes += 1
    elif vote == "down":
        p.downvotes += 1
    else:
        raise HTTPException(400, "Vote must be 'up' or 'down'")
    db.commit()
    return {"upvotes": p.upvotes, "downvotes": p.downvotes}


@router.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    p = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not p:
        raise HTTPException(404, "Post not found")
    if p.author_id != current_user.id and current_user.role not in ("admin", "authority"):
        raise HTTPException(403, "Not authorized")
    # Delete comments first
    db.query(ForumComment).filter(ForumComment.post_id == post_id).delete()
    db.delete(p)
    db.commit()
    return {"detail": "Deleted"}
