from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, Message
from schemas.message import (
    MessageCreate,
    MessageReplyCreate,
    MessageInboxResponse,
    MessageSendResponse,
    MessageReplyResponse,
)
from dependencies import get_current_user

router = APIRouter(prefix="/api/messages", tags=["messages"])


@router.post("", response_model=MessageSendResponse, status_code=201)
def send_message(
    msg_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if msg_data.receiver_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot send message to yourself")

    receiver = db.query(User).filter(User.id == msg_data.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    message = Message(
        sender_id=current_user.id,
        receiver_id=msg_data.receiver_id,
        content=msg_data.content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    return MessageSendResponse(
        id=message.id,
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        content=message.content,
        created_at=message.created_at,
    )


@router.get("", response_model=List[MessageInboxResponse])
def get_inbox(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = (
        db.query(Message, User.username)
        .join(User, Message.sender_id == User.id)
        .filter(Message.receiver_id == current_user.id)
        .order_by(Message.created_at.desc())
        .all()
    )

    inbox = []
    for message, sender_username in results:
        inbox.append(
            MessageInboxResponse(
                id=message.id,
                sender_id=message.sender_id,
                sender_username=sender_username,
                content=message.content,
                parent_id=message.parent_id,
                created_at=message.created_at,
                is_read=message.is_read,
            )
        )
        if not message.is_read:
            message.is_read = True

    db.commit()
    return inbox


@router.post("/{message_id}/reply", response_model=MessageReplyResponse, status_code=201)
def reply_message(
    message_id: int,
    reply_data: MessageReplyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    original = db.query(Message).filter(
        Message.id == message_id,
        Message.receiver_id == current_user.id,
    ).first()
    if not original:
        raise HTTPException(status_code=404, detail="Message not found")

    reply = Message(
        sender_id=current_user.id,
        receiver_id=original.sender_id,
        content=reply_data.content,
        parent_id=message_id,
    )
    db.add(reply)
    db.commit()
    db.refresh(reply)

    return MessageReplyResponse(
        id=reply.id,
        sender_id=reply.sender_id,
        receiver_id=reply.receiver_id,
        content=reply.content,
        parent_id=reply.parent_id,
        created_at=reply.created_at,
    )


@router.delete("/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.receiver_id == current_user.id,
    ).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    db.query(Message).filter(Message.parent_id == message_id).delete()
    db.delete(message)
    db.commit()
    return {"message": "Message deleted"}
