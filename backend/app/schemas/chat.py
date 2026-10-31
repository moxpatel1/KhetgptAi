"""
Chat and Conversation Schemas for KhetGPT
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class Citation(BaseModel):
    citation_id: int
    document_name: str
    page_number: int
    category: str = "Agriculture"
    similarity: float = 0.0

class ChatMessageRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=2000, description="Farmer query text")
    conversation_id: Optional[str] = Field(None, description="Optional conversation UUID for multi-turn chat")
    language: str = Field("en", description="'gu' for Gujarati, 'hi' for Hindi, 'en' for English")
    category: Optional[str] = Field(None, description="Optional category filter (e.g. 'Government Schemes')")

class ChatMessageResponse(BaseModel):
    conversation_id: str
    role: str = "assistant"
    content: str
    language: str
    citations: List[Citation] = []
    confidence: str = "High"
    evidence_found: bool = True
    provider: Optional[str] = None
    model: Optional[str] = None

class ConversationSummary(BaseModel):
    id: str
    title: str
    language: str
    created_at: datetime
    message_count: int = 0

class MessageItem(BaseModel):
    id: str
    role: str
    content: str
    language: str
    citations: Optional[List[Dict[str, Any]]] = None
    created_at: datetime

class ConversationDetail(BaseModel):
    id: str
    title: str
    language: str
    created_at: datetime
    messages: List[MessageItem] = []

