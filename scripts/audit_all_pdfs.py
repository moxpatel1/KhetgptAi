import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

import pypdf
from backend.app.services.rag.embeddings import VectorStore

store = VectorStore.get_instance()
indexed_stats = store.get_indexed_stats()
indexed_files = set(indexed_stats.get('documents', []))

folders = [
    ("Schemes", "Government Schemes"),
    ("Director of homiculture", "Horticulture & Crops"),
    ("Pashu palan", "Animal Husbandry & Dairy"),
    ("Bagayat", "Horticulture Schemes"),
    ("ICAR BOOks", "ICAR Agricultural Research"),
    ("Khetivadi", "State Agriculture Guidance")
]

print(f"Total chunks currently in ChromaDB: {store.count()}")
print(f"Total documents currently in ChromaDB: {len(indexed_files)}\n")

results = []

for folder, cat in folders:
    if not os.path.exists(folder):
        print(f"FOLDER NOT FOUND: {folder}")
        continue
    
    files = [f for f in os.listdir(folder) if f.lower().endswith('.pdf')]
    print(f"\n==========================================")
    print(f"Folder: {folder} ({len(files)} PDFs) - Category: {cat}")
    print(f"==========================================")
    
    for filename in sorted(files):
        path = os.path.join(folder, filename)
        is_indexed = filename in indexed_files
        size_mb = os.path.getsize(path) / (1024 * 1024)
        
        char_count = 0
        pages_count = 0
        status = "UNKNOWN"
        sample = ""
        
        try:
            reader = pypdf.PdfReader(path)
            pages_count = len(reader.pages)
            # Sample up to first 5 pages
            for p in reader.pages[:5]:
                txt = (p.extract_text() or "").strip()
                char_count += len(txt)
                if not sample and txt:
                    sample = " ".join(txt.split())[:120]
                    
            if char_count == 0:
                status = "SCANNED_EMPTY (0 text chars)"
            elif "/aguj" in sample or "s{Y" in sample or "Œhefu" in sample:
                status = f"LEGACY_FONT/GLYPH ({char_count} raw chars sampled)"
            elif any(ord(c) >= 0x0A80 and ord(c) <= 0x0AFF for c in sample):
                status = f"CLEAN_GUJARATI ({char_count} chars sampled)"
            elif any(ord(c) >= 0x0900 and ord(c) <= 0x097F for c in sample):
                status = f"CLEAN_HINDI ({char_count} chars sampled)"
            else:
                status = f"CLEAN_ENGLISH ({char_count} chars sampled)"
                
        except Exception as e:
            status = f"ERROR: {str(e)[:50]}"
            
        indexed_mark = "[INDEXED]" if is_indexed else "[NOT INDEXED]"
        print(f"  {indexed_mark} {filename} ({size_mb:.2f} MB, {pages_count} pgs): {status}")
        if sample:
            print(f"      Snippet: {sample[:100]}...")

