from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas import MessageRequest, Message, DeleteMessagesRequest
from app.db import get_db
from app.services import (
    create_message_service,
    fetch_unread_messages_service,
    delete_message_service,
    delete_multiple_messages_service,
    fetch_messages_service,
)

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=Message)
def submit_message(msg: MessageRequest, db: Session = Depends(get_db)):
    return create_message_service(msg, db)


@router.get("/unread", response_model=List[Message])
def fetch_unread_messages(
    recipient: Optional[str] = None, db: Session = Depends(get_db)
):
    return fetch_unread_messages_service(recipient, db)


@router.delete("/batch")
def remove_multiple_messages(
    request: DeleteMessagesRequest, db: Session = Depends(get_db)
):
    return delete_multiple_messages_service(request, db)


@router.delete("/{message_id}")
def remove_message_by_id(message_id: int, db: Session = Depends(get_db)):
    return delete_message_service(message_id, db)


@router.get("/", response_model=List[Message])
def fetch_messages(
    recipient: Optional[str] = None,
    start: int = 0,
    stop: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return fetch_messages_service(recipient, start, stop, db)
