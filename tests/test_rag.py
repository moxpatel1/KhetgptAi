"""
Automated Unit and Integration Tests for RAG Knowledge Base Pipeline
"""

import os
import pytest
from backend.app.services.rag.extractor import extract_text_from_pdf, compute_file_hash
from backend.app.services.rag.chunker import chunk_text, build_document_chunks
from backend.app.services.rag.embeddings import VectorStore
from backend.app.services.rag.retriever import HybridRetriever, expand_query

def test_chunker_basic():
    sample_text = (
        "Pradhan Mantri Fasal Bima Yojana (PMFBY) aims to support sustainable production in agriculture sector. "
        "It provides financial support to farmers suffering crop loss or damage arising out of unforeseen events. "
        "The scheme covers food crops, oilseeds, and annual commercial/horticultural crops."
    )
    chunks = chunk_text(sample_text, chunk_size=100, overlap=20)
    assert len(chunks) >= 1
    assert "PMFBY" in chunks[0]

def test_query_expansion():
    # Test Gujarati expansion
    gu_expanded = expand_query("પીએમ કિસાન યોજના")
    assert "PM-KISAN" in gu_expanded

    # Test Hindi expansion
    hi_expanded = expand_query("फसल बीमा क्लेम")
    assert "PMFBY" in hi_expanded

def test_vector_store_and_retrieval():
    vs = VectorStore.get_instance()
    assert vs is not None
    
    # Test embedding generation
    embeddings = vs.embed_texts(["Pradhan Mantri Fasal Bima Yojana"])
    assert len(embeddings) == 1
    assert len(embeddings[0]) == 384, f"Expected 384-d vector, got {len(embeddings[0])}"

    # Test retrieval
    retriever = HybridRetriever(vector_store=vs)
    results = retriever.retrieve("PM-KISAN installment eligibility", top_k=2)
    assert isinstance(results, list)

