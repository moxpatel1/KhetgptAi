"""
KhetGPT AI Chat API Router
Handles multi-turn conversational AI, hybrid RAG retrieval, citations,
and strict language enforcement for Gujarati, Hindi, and English.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.db_models import Conversation, Message
from backend.app.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ConversationSummary,
    ConversationDetail,
    MessageItem
)
from backend.app.services.rag.retriever import HybridRetriever
from backend.app.services.rag.generator import RAGAnswerGenerator

logger = logging.getLogger("khetgpt.api.chat")
router = APIRouter(prefix="/api", tags=["KhetGPT AI Chat"])

retriever = HybridRetriever()
generator = RAGAnswerGenerator()

@router.post("/chat", response_model=ChatMessageResponse)
def handle_chat_message(
    request: ChatMessageRequest,
    db: Session = Depends(get_db)
):
    """
    Main KhetGPT AI interaction endpoint.
    Performs hybrid retrieval against official agricultural knowledge base,
    enforces explicit user language, and generates cited answer.
    """
    # 1. Fetch or initialize conversation
    conv = None
    if request.conversation_id:
        conv = db.query(Conversation).filter(Conversation.id == request.conversation_id).first()

    if not conv:
        # Generate initial title from query snippet
        title = request.question.strip()[:40] + ("..." if len(request.question) > 40 else "")
        conv = Conversation(
            title=title,
            language=request.language
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)

    # 2. Save user message
    user_msg = Message(
        conversation_id=conv.id,
        role="user",
        content=request.question,
        language=request.language
    )
    db.add(user_msg)
    db.commit()

    # 3. Retrieve conversation history for context
    history_records = db.query(Message).filter(Message.conversation_id == conv.id).order_by(Message.created_at.asc()).all()
    history = [{"role": m.role, "content": m.content} for m in history_records[:-1]]  # exclude latest

    # 4. Hybrid RAG retrieval
    try:
        retrieved_chunks = retriever.retrieve(
            query=request.question,
            top_k=4,
            category=request.category
        )
    except Exception as e:
        logger.error(f"RAG retrieval error: {e}")
        retrieved_chunks = []

    # 5. Generate Grounded Answer with Language Enforcement
    gen_result = generator.generate_answer(
        question=request.question,
        retrieved_chunks=retrieved_chunks,
        language=request.language,
        conversation_history=history
    )

    # 6. Save Assistant Response with citations
    assistant_msg = Message(
        conversation_id=conv.id,
        role="assistant",
        content=gen_result["answer"],
        language=request.language,
        citations=gen_result["citations"]
    )
    db.add(assistant_msg)
    db.commit()

    return ChatMessageResponse(
        conversation_id=conv.id,
        role="assistant",
        content=gen_result["answer"],
        language=request.language,
        citations=gen_result["citations"],
        confidence=gen_result.get("confidence", "High"),
        evidence_found=gen_result.get("evidence_found", True),
        provider=gen_result.get("provider_used"),
        model=gen_result.get("model_used")
    )

@router.get("/conversations", response_model=List[ConversationSummary])
def list_conversations(db: Session = Depends(get_db)):
    """Lists persistent conversations for the user sidebar."""
    convs = db.query(Conversation).order_by(Conversation.updated_at.desc()).all()
    summaries = []
    for c in convs:
        summaries.append(ConversationSummary(
            id=c.id,
            title=c.title,
            language=c.language,
            created_at=c.created_at,
            message_count=len(c.messages)
        ))
    return summaries

@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
def get_conversation_detail(conversation_id: str, db: Session = Depends(get_db)):
    """Fetches full message history of a conversation."""
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = [
        MessageItem(
            id=m.id,
            role=m.role,
            content=m.content,
            language=m.language,
            citations=m.citations,
            created_at=m.created_at
        )
        for m in conv.messages
    ]

    return ConversationDetail(
        id=conv.id,
        title=conv.title,
        language=conv.language,
        created_at=conv.created_at,
        messages=messages
    )

@router.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """Deletes a conversation."""
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db.delete(conv)
    db.commit()
    return {"success": True, "message": "Conversation deleted successfully."}

