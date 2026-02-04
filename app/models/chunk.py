from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.connection import Base
import uuid
from datetime import datetime


class Chunk(Base):
    __tablename__ = "chunks"
