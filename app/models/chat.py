from sqlalchemy import Column, Text, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from app.database.connection import Base
import uuid
from datetime import datetime


class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    document_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Chat(id={self.id}, query={self.query[:50]}...)>"
