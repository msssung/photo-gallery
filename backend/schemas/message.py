from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageCreate(BaseModel):
    receiver_id: int
    content: str


class MessageReplyCreate(BaseModel):
    content: str


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
