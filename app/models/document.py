from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.connection import Base
import uuid
from datetime import datetime


class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    file_name = Column(String(255), nullable=False)
    file_size_mb = Column(Float, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    total_chunks = Column(Integer, nullable=False)

    chunks = relationship("Chunk", back_populates="document")

    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename})>"
