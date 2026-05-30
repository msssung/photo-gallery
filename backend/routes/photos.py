import uuid
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import User, Photo
from schemas.photo import PhotoResponse, PhotoUploadResponse, PhotoUpdate, PhotoUpdateResponse
from dependencies import get_current_user
from config import UPLOAD_DIR

router = APIRouter(prefix="/api/photos", tags=["photos"])


def _build_photo_response(photo: Photo, username: str) -> PhotoResponse:
    return PhotoResponse(
        id=photo.id,
        user_id=photo.user_id,
        username=username,
        image_url=f"/uploads/{photo.image_path}",
        description=photo.description,
        keywords=photo.keywords,
        created_at=photo.created_at,
    )


@router.get("/search", response_model=List[PhotoResponse])
def search_photos(keyword: str, db: Session = Depends(get_db)):
    results = (
        db.query(Photo, User.username)
        .join(User, Photo.user_id == User.id)
        .filter(Photo.keywords.ilike(f"%{keyword}%"))
        .all()
    )
    return [_build_photo_response(photo, username) for photo, username in results]


@router.get("", response_model=List[PhotoResponse])
def get_photos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = (
        db.query(Photo, User.username)
        .join(User, Photo.user_id == User.id)
        .order_by(Photo.created_at.desc())
        .all()
    )
    return [_build_photo_response(photo, username) for photo, username in results]


@router.post("", response_model=PhotoUploadResponse, status_code=201)
async def upload_photo(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    keywords: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    ext = os.path.splitext(file.filename)[1] if file.filename else ""
    filename = f"{uuid.uuid4()}{ext}"
    file_path = UPLOAD_DIR / filename

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    photo = Photo(
        user_id=current_user.id,
        image_path=filename,
        description=description,
        keywords=keywords,
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)

    return PhotoUploadResponse(
        id=photo.id,
        image_url=f"/uploads/{filename}",
        description=photo.description,
        keywords=photo.keywords,
    )


@router.put("/{photo_id}", response_model=PhotoUpdateResponse)
def update_photo(
    photo_id: int,
    update_data: PhotoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    if photo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if update_data.description is not None:
        photo.description = update_data.description
    if update_data.keywords is not None:
        photo.keywords = update_data.keywords

    db.commit()
    db.refresh(photo)
    return PhotoUpdateResponse(
        id=photo.id,
        description=photo.description,
        keywords=photo.keywords,
    )
