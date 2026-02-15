from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceResponse

router = APIRouter(prefix="/api/resources", tags=["Resources"])


@router.get("/", response_model=list[ResourceResponse])
def list_resources(
    course_code: str | None = None,
    resource_type: str | None = None,
    exam_type: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Resource)
    if course_code:
        q = q.filter(Resource.course_code == course_code)
    if resource_type:
        q = q.filter(Resource.resource_type == resource_type)
    if exam_type:
        q = q.filter(Resource.exam_type == exam_type)
    resources = q.order_by(Resource.created_at.desc()).all()
    return [
        ResourceResponse(
            id=r.id,
            title=r.title,
            description=r.description,
            file_url=r.file_url,
            course_code=r.course_code,
            year=r.year,
            exam_type=r.exam_type,
            resource_type=r.resource_type,
            tags=r.tags,
            uploaded_by=r.uploaded_by,
            uploader_name=r.uploader.name if r.uploader else None,
            created_at=r.created_at,
        )
        for r in resources
    ]


@router.post("/", response_model=ResourceResponse)
def create_resource(
    data: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    r = Resource(
        title=data.title,
        description=data.description,
        file_url=data.file_url,
        course_code=data.course_code,
        year=data.year,
        exam_type=data.exam_type,
        resource_type=data.resource_type,
        tags=data.tags,
        uploaded_by=current_user.id,
    )
    db.add(r)
    db.commit()
    db.refresh(r)
    return ResourceResponse(
        id=r.id,
        title=r.title,
        description=r.description,
        file_url=r.file_url,
        course_code=r.course_code,
        year=r.year,
        exam_type=r.exam_type,
        resource_type=r.resource_type,
        tags=r.tags,
        uploaded_by=r.uploaded_by,
        uploader_name=current_user.name,
        created_at=r.created_at,
    )


@router.delete("/{resource_id}")
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    r = db.query(Resource).filter(Resource.id == resource_id).first()
    if not r:
        raise HTTPException(404, "Resource not found")
    if r.uploaded_by != current_user.id and current_user.role not in ("admin", "authority"):
        raise HTTPException(403, "Not authorized")
    db.delete(r)
    db.commit()
    return {"detail": "Deleted"}
