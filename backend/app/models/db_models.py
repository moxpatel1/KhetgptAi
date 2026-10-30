"""
SQLAlchemy Database Models for KhetGPT
Stores Conversations, Messages, Crop Disease Scans, and Document Metadata.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, Boolean, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from backend.app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), default="New Inquiry")
    language = Column(String(10), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")

class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    language = Column(String(10), default="en")
    citations = Column(JSON, nullable=True)  # List of citations: [{"document_name": "...", "page_number": 1}]
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")

class DiseaseScan(Base):
    __tablename__ = "disease_scans"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    crop_name = Column(String(100), nullable=False)
    disease_name = Column(String(150), nullable=False)
    raw_class = Column(String(150), nullable=False)
    confidence = Column(Float, nullable=False)
    is_uncertain = Column(Boolean, default=False)
    is_healthy = Column(Boolean, default=False)
    language = Column(String(10), default="en")
    treatment_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    filename = Column(String(255), nullable=False, unique=True)
    folder = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    doc_hash = Column(String(64), nullable=False)
    page_count = Column(Integer, default=0)
    chunk_count = Column(Integer, default=0)
    status = Column(String(50), default="completed")  # 'queued', 'processing', 'completed', 'failed'
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

