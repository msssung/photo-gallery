from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PhotoResponse(BaseModel):
    id: int
    user_id: int
    username: str
    image_url: str
    description: Optional[str] = None
    keywords: Optional[str] = None
    created_at: datetime


class PhotoUploadResponse(BaseModel):
    id: int
    image_url: str
    description: Optional[str] = None
    keywords: Optional[str] = None


class PhotoUpdate(BaseModel):
    description: Optional[str] = None
    keywords: Optional[str] = None


class PhotoUpdateResponse(BaseModel):
    id: int
    description: Optional[str] = None
    keywords: Optional[str] = None
