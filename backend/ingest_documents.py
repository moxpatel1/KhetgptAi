"""
KhetGPT Agricultural Document Ingestion Pipeline
Processes authentic government PDFs across Schemes, Horticulture, Animal Husbandry,
ICAR Research, and Crop Protection into the persistent vector database.
"""

import os
import sys
import time
import logging
from typing import List, Dict, Any

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.services.rag.extractor import extract_text_from_pdf, compute_file_hash
from backend.app.services.rag.chunker import build_document_chunks
from backend.app.services.rag.embeddings import VectorStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("khetgpt.ingest")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

TARGET_DIRECTORIES = [
    {"folder": "Schemes", "category": "Government Schemes"},
    {"folder": "Director of homiculture", "category": "Horticulture & Crops"},
    {"folder": "Pashu palan", "category": "Animal Husbandry & Dairy"},
    {"folder": "Bagayat", "category": "Horticulture Schemes"},
    {"folder": "ICAR BOOks", "category": "ICAR Agricultural Research"},
    {"folder": "Khetivadi", "category": "State Agriculture Guidance"}
]

def ingest_all_documents(max_pages_per_doc: int = 40):
    print("=" * 60)
    print("KHETGPT - AGRICULTURAL DOCUMENT INGESTION PIPELINE")
    print("=" * 60)

    vector_store = VectorStore.get_instance()
    total_docs_processed = 0
    total_pages_extracted = 0
    total_chunks_indexed = 0
    failures = []

    t_start = time.time()

    for target in TARGET_DIRECTORIES:
        folder_name = target["folder"]
        category = target["category"]
        folder_path = os.path.join(PROJECT_ROOT, folder_name)

        if not os.path.exists(folder_path):
            logger.warning(f"Directory not found: {folder_path}")
            continue

        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
        logger.info(f"Scanning '{folder_name}' ({len(pdf_files)} PDFs, Category: {category})...")

        for f_idx, filename in enumerate(pdf_files):
            file_path = os.path.join(folder_path, filename)
            try:
                doc_hash = compute_file_hash(file_path)
                pages = extract_text_from_pdf(file_path, max_pages=max_pages_per_doc, enable_ocr=False)
                
                content_pages = [p for p in pages if p["has_content"]]
                if not content_pages:
                    logger.warning(f"No extractable text found in {filename} (might be pure scan/image).")
                    failures.append({"filename": filename, "folder": folder_name, "reason": "No extractable text / scanned image"})
                    continue

                chunks = build_document_chunks(
                    pages=content_pages,
                    doc_id=doc_hash[:12],
                    filename=filename,
                    category=category,
                    subfolder=folder_name,
                    chunk_size=700,
                    overlap=120
                )

                if chunks:
                    vector_store.add_chunks(chunks)
                    total_docs_processed += 1
                    total_pages_extracted += len(content_pages)
                    total_chunks_indexed += len(chunks)
                    logger.info(f"[{total_docs_processed}] {filename}: {len(content_pages)} pages, {len(chunks)} chunks indexed.")

            except Exception as e:
                logger.error(f"Failed processing {filename}: {e}")
                failures.append({"filename": filename, "folder": folder_name, "reason": str(e)})

    elapsed = time.time() - t_start
    print("=" * 60)
    print("INGESTION REPORT:")
    print(f"  Total Documents Successfully Indexed: {total_docs_processed}")
    print(f"  Total Pages Extracted:                {total_pages_extracted}")
    print(f"  Total Chunks Created & Stored:        {total_chunks_indexed}")
    print(f"  Failed / Unextractable Documents:     {len(failures)}")
    print(f"  Total Elapsed Time:                   {elapsed:.2f} seconds")
    print(f"  Current ChromaDB Total Chunks:        {vector_store.count()}")
    print("=" * 60)

    # Save ingestion summary JSON
    summary_path = os.path.join(PROJECT_ROOT, "data", "ingestion_summary.json")
    import json
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_documents_indexed": total_docs_processed,
            "total_pages_extracted": total_pages_extracted,
            "total_chunks_stored": total_chunks_indexed,
            "chroma_total_count": vector_store.count(),
            "failures": failures,
            "elapsed_seconds": round(elapsed, 2)
        }, f, indent=2)
    print(f"Saved ingestion summary to {summary_path}")

if __name__ == "__main__":
    ingest_all_documents()

