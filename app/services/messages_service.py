from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud.messages_crud import (
    create_message,
    get_unread_messages,
    mark_messages_as_read_by_recipient,
    delete_messages_by_ids,
    delete_messages_by_recipients,
    delete_messages_by_ids_and_recipients,
    get_messages,
)
from app.schemas import MessageRequest, DeleteMessagesRequest
from app.models import Message


def create_message_service(msg: MessageRequest, db: Session) -> Message:
    """
    Submit message to a recipient
    """
    if not msg.recipient:
        raise HTTPException(status_code=400, detail="Recipient cannot be empty")
    if not msg.text:
        raise HTTPException(status_code=400, detail="Message text cannot be empty")
    return create_message(db, msg)


def fetch_unread_messages_service(
    recipient: Optional[str], db: Session
) -> List[Message]:
    """
    Fetch unread messages for a recipient or all recipients if recipient is None
    """
    if recipient is not None and not isinstance(recipient, str):
        raise HTTPException(
            status_code=400, detail="Recipient ID must be a string or None"
        )
    unread_messages = get_unread_messages(db, recipient)
    if len(unread_messages):
        mark_messages_as_read_by_recipient(db, recipient)
    return unread_messages


def delete_message_service(message_id: int, db: Session):
    """
    Delete a single message by id
    """
    if not isinstance(message_id, int) or message_id <= 0:
        raise HTTPException(
            status_code=400, detail="Message ID must be a positive integer"
        )

    message_id_list = [message_id]

    return delete_messages_by_ids(db, message_id_list)


def delete_multiple_messages_service(request: DeleteMessagesRequest, db: Session):
    """
    Delete messages by IDs or recipients
    """
    if not request.message_ids and not request.recipients:
        raise HTTPException(
            status_code=400,
            detail="You must provide either 'message_ids' or 'recipients' for deletion.",
        )

    if request.message_ids and any(id <= 0 for id in request.message_ids):
        raise HTTPException(
            status_code=400,
            detail="All message IDs must be positive integers greater than 0.",
        )

    if request.message_ids and request.recipients:
        return delete_messages_by_ids_and_recipients(
            db, request.message_ids, request.recipients
        )

    if request.message_ids:
        return delete_messages_by_ids(db, request.message_ids)

    if request.recipients:
        return delete_messages_by_recipients(db, request.recipients)


def fetch_messages_service(
    recipient: Optional[str], start: int, stop: Optional[int], db: Session
) -> List[Message]:
    """
    Fetch all messages for a recipient or all recipients if recipient is None. (with optional pagination)
    """
    if start < 0:
        raise HTTPException(
            status_code=400, detail="Start index should be 0 or greater"
        )

    if stop is not None:
        if stop > 0 and stop <= start:
            raise HTTPException(
                status_code=400,
                detail="Stop index can't be less than or equal to start index",
            )
        elif stop <= 0:
            raise HTTPException(
                status_code=400, detail="Stop index should be greater than 0"
            )

    messages = get_messages(db, recipient, start, stop)
    if len(messages) > 0:
        mark_messages_as_read_by_recipient(db, recipient)
    return messages
