from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class MessageRequest(BaseModel):
    recipient: str
    text: str


class Message(BaseModel):
    id: int
    recipient: str
    text: str
    is_read: bool
    created_at: datetime


class DeleteMessagesRequest(BaseModel):
    message_ids: Optional[List[int]] = None
    recipients: Optional[List[str]] = None
