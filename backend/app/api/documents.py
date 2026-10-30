"""
Document Ingestion & Knowledge Base Management API Router
"""

import os
import shutil
import logging
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.db_models import DocumentMetadata
from backend.app.schemas.documents import DocumentUploadResponse, KnowledgeBaseStats
from backend.app.services.rag.extractor import extract_text_from_pdf, compute_file_hash
from backend.app.services.rag.chunker import build_document_chunks
from backend.app.services.rag.embeddings import VectorStore

logger = logging.getLogger("khetgpt.api.documents")
router = APIRouter(prefix="/api/documents", tags=["Agricultural Documents"])

DATA_UPLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "uploads"))
os.makedirs(DATA_UPLOADS_DIR, exist_ok=True)

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_and_index_document(
    file: UploadFile = File(...),
    category: str = Form("Government Schemes"),
    db: Session = Depends(get_db)
):
    """
    Uploads a new agricultural PDF, extracts text, chunks,
    generates embeddings, and indexes into ChromaDB.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF documents are supported.")

    file_path = os.path.join(DATA_UPLOADS_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc_hash = compute_file_hash(file_path)

    # Check if duplicate already exists
    existing = db.query(DocumentMetadata).filter(DocumentMetadata.doc_hash == doc_hash).first()
    if existing and existing.status == "completed":
        return DocumentUploadResponse(
            success=True,
            filename=file.filename,
            doc_id=existing.id,
            pages_extracted=existing.page_count,
            chunks_created=existing.chunk_count,
            category=existing.category,
            message="Document has already been indexed in the knowledge base."
        )

    # Extract text
    pages = extract_text_from_pdf(file_path, enable_ocr=True)
    content_pages = [p for p in pages if p["has_content"]]

    if not content_pages:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from this PDF. It may be an encrypted or unreadable scan."
        )

    # Chunk text
    chunks = build_document_chunks(
        pages=content_pages,
        doc_id=doc_hash[:12],
        filename=file.filename,
        category=category,
        subfolder="Uploads",
        chunk_size=700,
        overlap=120
    )

    # Index into Vector DB
    vector_store = VectorStore.get_instance()
    vector_store.add_chunks(chunks)

    # Save to database
    meta = DocumentMetadata(
        filename=file.filename,
        folder="Uploads",
        category=category,
        doc_hash=doc_hash,
        page_count=len(content_pages),
        chunk_count=len(chunks),
        status="completed"
    )
    db.add(meta)
    db.commit()
    db.refresh(meta)

    return DocumentUploadResponse(
        success=True,
        filename=file.filename,
        doc_id=meta.id,
        pages_extracted=len(content_pages),
        chunks_created=len(chunks),
        category=category,
        message=f"Successfully extracted {len(content_pages)} pages and indexed {len(chunks)} chunks."
    )

@router.get("/stats", response_model=KnowledgeBaseStats)
def get_knowledge_base_stats():
    """Returns knowledge base statistics and list of indexed documents."""
    vector_store = VectorStore.get_instance()
    stats = vector_store.get_indexed_stats()
    return KnowledgeBaseStats(
        total_chunks=stats.get("total_chunks", 0),
        total_documents=stats.get("total_documents", 0),
        documents=stats.get("documents", []),
        categories=stats.get("categories", [])
    )

@router.get("/list")
def list_documents(db: Session = Depends(get_db)):
    """Lists all registered documents in the database."""
    docs = db.query(DocumentMetadata).order_by(DocumentMetadata.created_at.desc()).all()
    return docs

