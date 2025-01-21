from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from app.models import Message
from app.schemas import MessageRequest
from datetime import datetime


def create_message(db: Session, msg: MessageRequest) -> Message:
    new_message = Message(
        recipient=msg.recipient,
        text=msg.text,
        is_read=False,
        created_at=datetime.utcnow(),
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


def get_unread_messages(db: Session, recipient: Optional[str] = None) -> List[Message]:
    query = db.query(Message).filter(Message.is_read == False)
    if recipient:
        query = query.filter(Message.recipient == recipient)
    return query.all()


def mark_messages_as_read_by_recipient(
    db: Session, recipient: Optional[str] = None
) -> None:
    query = db.query(Message).filter(Message.is_read == False)
    if recipient:
        query = query.filter(Message.recipient == recipient)
    query.update({Message.is_read: True}, synchronize_session=False)
    db.commit()


def delete_message(db: Session, message_id: int):
    msg = db.query(Message).filter(Message.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(msg)
    db.commit()
    return msg


def delete_messages_by_ids(db: Session, message_ids: List[int]):
    existing_ids = db.query(Message.id).filter(Message.id.in_(message_ids)).all()
    existing_ids = {id_tuple[0] for id_tuple in existing_ids}  # Extract IDs from tuples

    missing_ids = set(message_ids) - existing_ids
    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Messages with the following IDs were not found: {missing_ids}",
        )

    db.query(Message).filter(Message.id.in_(message_ids)).delete(
        synchronize_session=False
    )
    db.commit()
    return {"detail": f"Deleted {len(message_ids)} messages."}


def delete_messages_by_recipients(db: Session, recipients: List[str]):
    existing_recipients = (
        db.query(Message.recipient).filter(Message.recipient.in_(recipients)).all()
    )
    existing_recipients = {
        recipient_tuple[0] for recipient_tuple in existing_recipients
    }  # Extract recipients from tuples

    missing_recipients = set(recipients) - existing_recipients
    if missing_recipients:
        raise HTTPException(
            status_code=404,
            detail=f"Messages with the following recipients were not found: {missing_recipients}",
        )

    db.query(Message).filter(Message.recipient.in_(recipients)).delete(
        synchronize_session=False
    )
    db.commit()
    return {"detail": f"Deleted messages for {len(existing_recipients)} recipients."}


def delete_messages_by_ids_and_recipients(
    db: Session, message_ids: List[int], recipients: List[str]
):
    existing_messages = (
        db.query(Message)
        .filter(or_(Message.id.in_(message_ids), Message.recipient.in_(recipients)))
        .all()
    )

    if not existing_messages:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Some message IDs and recipients were not found.",
                "missing_ids": list(message_ids),
                "missing_recipients": list(recipients),
            },
        )

    db.query(Message).filter(
        or_(Message.id.in_(message_ids), Message.recipient.in_(recipients))
    ).delete(synchronize_session=False)
    db.commit()

    return {
        "detail": f"Deleted {len(existing_messages)} messages matching IDs or recipients."
    }


def get_messages(
    db: Session, recipient: Optional[str], start: int, stop: Optional[int]
) -> List[Message]:
    query = db.query(Message).order_by(Message.created_at)

    if recipient is not None:
        query = query.filter(Message.recipient == recipient)

    if stop is not None:
        return query.offset(start).limit(stop - start).all()
    return query.offset(start).all()
