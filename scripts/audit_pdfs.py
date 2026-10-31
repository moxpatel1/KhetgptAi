"""
Comprehensive Audit of All Agricultural PDFs in KhetGPT
Audits 79 agricultural PDF documents across 6 domain directories.
Checks:
- Filename, Folder, File size (MB)
- Open status, Page count
- Extractable text length
- Document status (Digital Text / Scanned Image / OCR Required)
- Chunks indexed in ChromaDB
- Searchability
"""

import os
import sys
import json
from pypdf import PdfReader

# Ensure project root in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from backend.app.services.rag.embeddings import VectorStore

def audit_all_pdfs():
    vs = VectorStore.get_instance()
    records = vs.collection.get(include=["metadatas"])
    metas = records["metadatas"] if records else []
    
    chunk_counts = {}
    for m in metas:
        if m:
            fn = m.get("filename") or m.get("pdf_name")
            if fn:
                chunk_counts[fn] = chunk_counts.get(fn, 0) + 1

    folders = ["Bagayat", "Director of homiculture", "ICAR BOOks", "Khetivadi", "Pashu palan", "Schemes"]
    inventory = []

    for folder in folders:
        fpath = os.path.join(PROJECT_ROOT, folder)
        if not os.path.exists(fpath):
            continue
        for fname in sorted(os.listdir(fpath)):
            if not fname.lower().endswith(".pdf"):
                continue
            fp = os.path.join(fpath, fname)
            size_mb = os.path.getsize(fp) / (1024 * 1024)
            
            num_pages = 0
            status = "Unknown"
            extracted_len = 0
            can_open = False
            error_msg = None
            
            try:
                reader = PdfReader(fp)
                can_open = True
                num_pages = len(reader.pages)
                sample_text = ""
                for p in reader.pages[:min(10, num_pages)]:
                    sample_text += (p.extract_text() or "") + " "
                extracted_len = len(sample_text.strip())
                if extracted_len > 100:
                    status = "Digital Text"
                else:
                    status = "Scanned Image"
            except Exception as e:
                error_msg = str(e)
                status = "Corrupted / Read Error"
                
            chunks_indexed = chunk_counts.get(fname, 0)
            
            inventory.append({
                "folder": folder,
                "filename": fname,
                "size_mb": round(size_mb, 2),
                "can_open": can_open,
                "page_count": num_pages,
                "status": status,
                "extracted_sample_len": extracted_len,
                "chunks_indexed": chunks_indexed,
                "is_indexed": chunks_indexed > 0,
                "error": error_msg
            })

    report_dir = os.path.join(PROJECT_ROOT, "data", "reports")
    os.makedirs(report_dir, exist_ok=True)
    report_file = os.path.join(report_dir, "pdf_audit_report.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)

    print("=" * 80)
    print("KHETGPT - 79 AGRICULTURAL PDF INVENTORY AUDIT")
    print("=" * 80)
    print(f"Total PDFs Audited:                 {len(inventory)}")
    print(f"Digital Text PDFs (Extractable):    {sum(1 for d in inventory if d['status'] == 'Digital Text')}")
    print(f"Scanned Image PDFs (Need OCR):      {sum(1 for d in inventory if d['status'] == 'Scanned Image')}")
    print(f"Corrupted PDFs:                     {sum(1 for d in inventory if d['status'].startswith('Corrupted'))}")
    print(f"Currently Indexed in ChromaDB:      {sum(1 for d in inventory if d['is_indexed'])}")
    print(f"Unindexed Digital Text PDFs:        {sum(1 for d in inventory if d['status'] == 'Digital Text' and not d['is_indexed'])}")
    print(f"Total ChromaDB Chunks:              {vs.count()}")
    print("=" * 80)

    unindexed_docs = [d for d in inventory if not d["is_indexed"]]
    print(f"\nUNINDEXED DOCUMENTS ({len(unindexed_docs)}):")
    for d in unindexed_docs:
        print(f"  - [{d['folder']}] {d['filename']} ({d['status']}, {d['page_count']} pages, {d['size_mb']} MB)")

if __name__ == "__main__":
    audit_all_pdfs()
