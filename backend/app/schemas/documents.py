"""
Document Ingestion & Knowledge Base Schemas
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class DocumentUploadResponse(BaseModel):
    success: bool
    filename: str
    doc_id: str
    pages_extracted: int
    chunks_created: int
    category: str
    message: str

class KnowledgeBaseStats(BaseModel):
    total_chunks: int
    total_documents: int
    documents: List[str]
    categories: List[str]

