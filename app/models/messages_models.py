from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.db import Base


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    recipient = Column(String(255), index=True)
    text = Column(String(255))
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
