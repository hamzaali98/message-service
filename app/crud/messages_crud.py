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
    query.update({Message.is_read: True}, synchronize_session="fetch")
    db.commit()


def delete_messages_by_ids(db: Session, message_ids: List[int]):
    # Find IDs that exist in the database
    existing_ids = db.query(Message.id).filter(Message.id.in_(message_ids)).all()
    existing_ids = {row[0] for row in existing_ids}

    missing_ids = set(message_ids) - existing_ids

    if not existing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"No messages found",
        )
    deleted_count = (
        db.query(Message)
        .filter(Message.id.in_(existing_ids))
        .delete(synchronize_session=False)
        or 0
    )
    db.commit()

    return {
        "detail": "Partial success" if missing_ids else "Success",
        "deleted_count": deleted_count,
        "missing_ids": list(missing_ids),
    }


def delete_messages_by_recipients(db: Session, recipients: List[str]):
    existing_recipients = (
        db.query(Message.recipient)
        .filter(Message.recipient.in_(recipients))
        .distinct()
        .all()
    )
    existing_recipients = {
        recipient_tuple[0] for recipient_tuple in existing_recipients
    }  # Extract recipients from tuples

    missing_recipients = set(recipients) - existing_recipients

    if not existing_recipients:
        raise HTTPException(
            status_code=404,
            detail=f"No messages found",
        )

    deleted_count = (
        db.query(Message)
        .filter(Message.recipient.in_(existing_recipients))
        .delete(synchronize_session=False)
    ) or 0
    db.commit()

    return {
        "detail": "Partial success" if missing_recipients else "Success",
        "deleted_count": deleted_count,
        "missing_recipients": list(missing_recipients),
    }


def delete_messages_by_ids_and_recipients(
    db: Session, message_ids: List[int], recipients: List[str]
):
    existing_ids = db.query(Message.id).filter(Message.id.in_(message_ids)).all()
    existing_ids = {row[0] for row in existing_ids}
    missing_ids = set(message_ids) - existing_ids

    existing_recipients = (
        db.query(Message.recipient)
        .filter(Message.recipient.in_(recipients))
        .distinct()
        .all()
    )
    existing_recipients = {row[0] for row in existing_recipients}
    missing_recipients = set(recipients) - existing_recipients

    if not existing_ids and not existing_recipients:
        raise HTTPException(
            status_code=404,
            detail=f"No messages found",
        )

    deleted_count = (
        db.query(Message)
        .filter(
            or_(
                Message.id.in_(existing_ids), Message.recipient.in_(existing_recipients)
            )
        )
        .delete(synchronize_session=False)
        or 0
    )

    db.commit()
    return {
        "detail": (
            "Partial success" if (missing_ids or missing_recipients) else "Success"
        ),
        "deleted_count": deleted_count,
        "missing_ids": list(missing_ids),
        "missing_recipients": list(missing_recipients),
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
