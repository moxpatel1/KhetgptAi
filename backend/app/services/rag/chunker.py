"""
KhetGPT Document Chunker
Splits extracted document pages into overlapping semantic chunks with rich metadata.
"""

import re
from typing import List, Dict, Any

def chunk_text(
    text: str,
    chunk_size: int = 700,
    overlap: int = 120
) -> List[str]:
    """
    Splits text into chunks of approximately chunk_size with overlap,
    respecting sentence boundaries (period, full stop, danda ।, question mark, newlines).
    """
    if not text or len(text.strip()) == 0:
        return []

    # If text is already shorter than chunk_size, return as single chunk
    if len(text) <= chunk_size:
        return [text]

    # Split into sentence segments
    sentences = re.split(r'(?<=[.।!?\n])\s+', text)
    chunks = []
    current_chunk = []
    current_len = 0

    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        
        sent_len = len(sent)
        if current_len + sent_len > chunk_size and current_chunk:
            combined = " ".join(current_chunk)
            chunks.append(combined)
            
            # Keep tail sentences for overlap
            overlap_sentences = []
            overlap_len = 0
            for s in reversed(current_chunk):
                if overlap_len + len(s) <= overlap:
                    overlap_sentences.insert(0, s)
                    overlap_len += len(s)
                else:
                    break
            current_chunk = overlap_sentences
            current_len = overlap_len

        current_chunk.append(sent)
        current_len += sent_len

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def build_document_chunks(
    pages: List[Dict[str, Any]],
    doc_id: str,
    filename: str,
    category: str,
    subfolder: str,
    chunk_size: int = 700,
    overlap: int = 120
) -> List[Dict[str, Any]]:
    """
    Takes extracted pages and returns a list of indexed chunk objects:
    [
        {
            "id": "doc_id_p1_c0",
            "text": "...",
            "metadata": {
                "doc_id": "...",
                "filename": "...",
                "page_number": 1,
                "category": "...",
                "subfolder": "...",
                "chunk_index": 0
            }
        }, ...
    ]
    """
    indexed_chunks = []

    for page in pages:
        p_num = page["page_number"]
        p_text = page["text"]
        if not page["has_content"]:
            continue

        page_chunks = chunk_text(p_text, chunk_size=chunk_size, overlap=overlap)
        for c_idx, c_text in enumerate(page_chunks):
            # Globally unique chunk ID using document hash prefix + page + chunk index
            chunk_id = f"doc_{doc_id}_p{p_num}_c{c_idx}"
            indexed_chunks.append({
                "id": chunk_id,
                "text": c_text,
                "metadata": {
                    "doc_id": doc_id,
                    "filename": filename,
                    "page_number": p_num,
                    "category": category,
                    "subfolder": subfolder,
                    "chunk_index": c_idx,
                    "char_count": len(c_text)
                }
            })

    return indexed_chunks
