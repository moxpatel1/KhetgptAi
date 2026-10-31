"""
Ingest Remaining Unindexed Agricultural Documents into ChromaDB
Processes the 20 unindexed digital text and OCR documents to achieve
full 100% coverage across all 79 agricultural publications.
"""

import os
import sys
import time
import hashlib
from typing import List, Dict, Any
from pypdf import PdfReader

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from backend.app.services.rag.embeddings import VectorStore
from backend.app.services.rag.chunker import build_document_chunks

# Documents to ingest with their metadata
DOCUMENTS_TO_INGEST = [
    # Director of homiculture
    {"folder": "Director of homiculture", "filename": "SUSHK VISTAR MA BAGAYATI PAKO NI KHETI - MAHISAGAR.pdf", "category": "Horticulture Schemes", "max_pages": 40},
    {"folder": "Director of homiculture", "filename": "Vermi Compost.pdf", "category": "Horticulture & Crops", "max_pages": 60},
    {"folder": "Director of homiculture", "filename": "sukshma piyat padhati.pdf", "category": "Horticulture & Crops", "max_pages": 60},
    
    # ICAR Books
    {"folder": "ICAR BOOks", "filename": "Farmers Innovations 2025 Hindi.pdf", "category": "ICAR Agricultural Research", "max_pages": 60},
    {"folder": "ICAR BOOks", "filename": "ICAR Insights Outcomes Booklet (Hindi) (2).pdf", "category": "ICAR Agricultural Research", "max_pages": 60},
    {"folder": "ICAR BOOks", "filename": "ICAR Transforming 2022_for web.pdf", "category": "ICAR Agricultural Research", "max_pages": 50},
    {"folder": "ICAR BOOks", "filename": "ICAR-En-Kharif-Agro-Advisories-for-Farmers-2025.pdf", "category": "ICAR Agricultural Research", "max_pages": 70},
    {"folder": "ICAR BOOks", "filename": "ICAR-Guidelines-PSF-2014_0.pdf", "category": "ICAR Agricultural Research", "max_pages": 50},
    {"folder": "ICAR BOOks", "filename": "Kheti_March_25 FINAL PRINT FILE (2).pdf", "category": "ICAR Agricultural Research", "max_pages": 60},
    {"folder": "ICAR BOOks", "filename": "PME_RPP-Guide-Lines.pdf", "category": "ICAR Agricultural Research", "max_pages": 40},
    {"folder": "ICAR BOOks", "filename": "Quality Manual_Oct 2025.pdf", "category": "ICAR Agricultural Research", "max_pages": 36},
    {"folder": "ICAR BOOks", "filename": "RULESANDBYELAWS.pdf", "category": "ICAR Agricultural Research", "max_pages": 40},
    {"folder": "ICAR BOOks", "filename": "farmerbook.pdf", "category": "ICAR Agricultural Research", "max_pages": 60},
    {"folder": "ICAR BOOks", "filename": "icarars.pdf", "category": "ICAR Agricultural Research", "max_pages": 50},
    {"folder": "ICAR BOOks", "filename": "icarpowers.pdf", "category": "ICAR Agricultural Research", "max_pages": 50},
    
    # Pashu palan annual administrative reports
    {"folder": "Pashu palan", "filename": "પશુપાલન ખાતાનો વાર્ષિક વહીવટી અહેવાલ વર્ષ ૨૦૨૦-૨૧.pdf", "category": "Animal Husbandry & Dairy", "max_pages": 60},
    {"folder": "Pashu palan", "filename": "પશુપાલન ખાતાનો વાર્ષિક વહીવટી અહેવાલ વર્ષ ૨૦૨૧-૨૦૨૨.pdf", "category": "Animal Husbandry & Dairy", "max_pages": 60},
    {"folder": "Pashu palan", "filename": "પશુપાલન ખાતાનો વાર્ષિક વહીવટી અહેવાલ વર્ષ ૨૦૨૨-૨૩.pdf", "category": "Animal Husbandry & Dairy", "max_pages": 60},
    
    # Schemes (OCR-extracted)
    {"folder": "Schemes", "filename": "English.pdf", "category": "Government Schemes", "ocr": True},
    {"folder": "Schemes", "filename": "NewSchemeAdd.pdf", "category": "Government Schemes", "ocr": True}
]

def extract_pages(file_path: str, max_pages: int = 50, ocr: bool = False) -> List[Dict[str, Any]]:
    pages = []
    if ocr:
        import pytesseract
        import pdfplumber
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        try:
            with pdfplumber.open(file_path) as pdf:
                for i, p in enumerate(pdf.pages):
                    img = p.to_image(resolution=150).original
                    txt = pytesseract.image_to_string(img, lang="eng")
                    clean = " ".join(txt.split()).replace("\x00", "")
                    if len(clean) > 30:
                        pages.append({
                            "page_number": i + 1,
                            "text": clean,
                            "char_count": len(clean),
                            "is_ocr": True,
                            "has_content": True
                        })
        except Exception as e:
            print(f"OCR extraction failed for {file_path}: {e}")
        return pages

    try:
        reader = PdfReader(file_path)
        total_p = len(reader.pages)
        limit = min(total_p, max_pages)
        for i in range(limit):
            t = reader.pages[i].extract_text() or ""
            clean = " ".join(t.split()).replace("\x00", "")
            if len(clean) > 30:
                pages.append({
                    "page_number": i + 1,
                    "text": clean,
                    "char_count": len(clean),
                    "is_ocr": False,
                    "has_content": True
                })
    except Exception as e:
        print(f"PDF extraction failed for {file_path}: {e}")
    return pages

def main():
    vs = VectorStore.get_instance()
    initial_count = vs.count()
    print(f"Starting ingestion. Initial ChromaDB chunks: {initial_count}")
    
    total_new_chunks = 0
    total_docs = 0
    t0 = time.time()

    for item in DOCUMENTS_TO_INGEST:
        folder = item["folder"]
        fname = item["filename"]
        category = item["category"]
        max_p = item.get("max_pages", 50)
        is_ocr = item.get("ocr", False)
        
        fpath = os.path.join(PROJECT_ROOT, folder, fname)
        if not os.path.exists(fpath):
            print(f"Skipping missing: {fpath}")
            continue
            
        print(f"Extracting [{folder}] {fname}...")
        pages = extract_pages(fpath, max_pages=max_p, ocr=is_ocr)
        if not pages:
            print(f"  -> No text extracted from {fname}")
            continue
            
        doc_id = hashlib.sha256(fname.encode("utf-8")).hexdigest()[:12]
        chunks = build_document_chunks(
            pages=pages,
            doc_id=doc_id,
            filename=fname,
            category=category,
            subfolder=folder,
            chunk_size=700,
            overlap=120
        )
        
        if chunks:
            vs.add_chunks(chunks, batch_size=64)
            total_new_chunks += len(chunks)
            total_docs += 1
            print(f"  -> Indexed {len(chunks)} chunks from {len(pages)} pages.")

    elapsed = time.time() - t0
    final_count = vs.count()
    print("=" * 60)
    print("INGESTION COMPLETE:")
    print(f"  Documents Processed:    {total_docs}")
    print(f"  New Chunks Added:       {total_new_chunks}")
    print(f"  ChromaDB Total Chunks:  {final_count} (was {initial_count})")
    print(f"  Elapsed Time:           {elapsed:.2f}s")
    print("=" * 60)

if __name__ == "__main__":
    main()

