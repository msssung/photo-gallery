from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class MessageCreate(BaseModel):
    receiver_id: int
    content: str

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Content cannot be empty")
        return v


class MessageReplyCreate(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Content cannot be empty")
        return v


class MessageInboxResponse(BaseModel):
    id: int
    sender_id: int
    sender_username: str
    content: str
    parent_id: Optional[int] = None
    created_at: datetime
    is_read: bool


class MessageSendResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    created_at: datetime


class MessageReplyResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    parent_id: Optional[int] = None
    created_at: datetime
