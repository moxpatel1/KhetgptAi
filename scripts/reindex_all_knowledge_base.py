"""
Memory-Safe Streaming Knowledge Base Indexer for KhetGPT
Streams and indexes all authentic agricultural literature across:
- Bagayat (Pomegranate, Guava, Lemon, Floriculture, Horticulture Schemes)
- Pashu palan (Animal Husbandry, Cow/Buffalo Breeds, Dairy Loans, Subsidies)
- Khetivadi (Wheat, Rice, Cotton, Groundnut, Sugarcane, Castor scientific PoP)
- Schemes (PM-KISAN, PMFBY, WBCIS, iKhedut)
- ICAR BOOks (Agro-advisories, Soil Testing Manual, Acid Soils, Farmer Innovations)
- Director of homiculture (Vegetables, Fruits, Greenhouses, Plant Protection)
"""

import os
import sys
import re
import time
import gc
import logging
from typing import List, Dict, Any, Generator

# Force UTF-8 on Windows
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from backend.app.services.rag.embeddings import VectorStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("khetgpt.reindex")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TRANSCRIPTS_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "transcripts")

PAGE_PATTERN = re.compile(r"--- \[DOCUMENT: (.*?) \| Subfolder: (.*?) \| Page: (\d+)\] ---")

# Ordered with pending domains first for fast completion
STREAM_SOURCES = [
    # 1. Farming Practices (Cotton, Wheat, Rice, Castor, Groundnut)
    ("khetivadi_scientific_crops_pop.txt", "https://agri.gujarat.gov.in", "State Agriculture Guidance", "Khetivadi"),
    
    # 2. Bagayat (Horticulture Schemes & Fruits - Guava, Lemon, Vegetables)
    ("bagayat_horticulture_fruits_pop.txt", "https://doh.gujarat.gov.in", "Horticulture Schemes", "Bagayat"),
    
    # 3. ICAR Agricultural Research & Soil Health Manual
    ("icar_agro_advisories_and_soil_testing.txt", "https://icar.org.in", "ICAR Agricultural Research", "ICAR BOOks"),

    # 4. Animal Husbandry & Livestock
    ("pashupalan_schemes_and_reports.txt", "https://doah.gujarat.gov.in", "Animal Husbandry & Dairy", "Pashu palan"),
    
    # 5. Schemes (PM-KISAN, PMFBY, iKhedut)
    ("schemes_pmfby_pmkisan_ikhedut.txt", "https://pmfby.gov.in", "Government Schemes", "Schemes"),
    
    # 6. Horticulture Plant Protection & Chemicals
    ("horticulture_plant_protection_chemicals.txt", "https://doh.gujarat.gov.in", "Horticulture & Crops", "Director of homiculture"),
]

STANDALONE_RAW = [
    ("pm_kisan_guidelines.txt", "PM-KISAN Guidelines", "PMKisanSamanNidhi.pdf", "https://pmkisan.gov.in", "Government Schemes", "Schemes"),
    ("pmfby_guidelines.txt", "PMFBY Operational Guidelines", "operational_guidelines_pmfby.pdf", "https://pmfby.gov.in", "Government Schemes", "Schemes"),
    ("ikhedut_guidelines_gu.txt", "iKhedut 2.0 Portal Guidelines", "iKhedut_2.0_User_Manual.pdf", "https://ikhedut.gujarat.gov.in", "Government Schemes", "Schemes"),
    ("soil_health_card.txt", "Soil Health Card Guidelines", "Book Methods manual (Soil Testing In India)001.pdf", "https://soilhealth.dac.gov.in", "ICAR Agricultural Research", "ICAR BOOks"),
    ("soil_health_card_macro_micro_data.txt", "Soil Health Nutrient Norms", "Soil_Health_Card_RKVY_Data.csv", "https://soilhealth.dac.gov.in", "ICAR Agricultural Research", "ICAR BOOks"),
]


def stream_chunks_from_file(raw_file: str, default_url: str, category: str, default_folder: str, max_pages: int = 400) -> Generator[Dict[str, Any], None, None]:
    path = os.path.join(TRANSCRIPTS_DIR, raw_file)
    if not os.path.exists(path):
        return

    chunk_size = 700
    overlap = 120

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    matches = list(PAGE_PATTERN.finditer(text))
    if max_pages and len(matches) > max_pages:
        matches = matches[:max_pages]

    for i, m in enumerate(matches):
        pdf_name = m.group(1).strip()
        subfolder = m.group(2).strip() or default_folder
        page_num = int(m.group(3))

        start_pos = m.end()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        page_text = text[start_pos:end_pos].strip()

        if not page_text or len(page_text) < 30:
            continue

        if len(page_text) <= chunk_size:
            sub_chunks = [page_text]
        else:
            sub_chunks = []
            pos = 0
            while pos < len(page_text):
                sub_chunks.append(page_text[pos:pos + chunk_size])
                pos += (chunk_size - overlap)

        source_title = pdf_name.replace(".pdf", "").replace("_", " ").title()

        for sc_idx, sc_text in enumerate(sub_chunks):
            clean_text = " ".join(sc_text.split())
            safe_pdf = re.sub(r"[^\w]", "_", pdf_name)[:12]
            chunk_id = f"tr_{subfolder[:4]}_{safe_pdf}_{page_num}_{sc_idx}_{i}"
            yield {
                "id": chunk_id,
                "text": clean_text,
                "metadata": {
                    "filename": pdf_name,
                    "pdf_name": pdf_name,
                    "page_number": page_num,
                    "subfolder": subfolder,
                    "source_name": source_title,
                    "source_url": default_url,
                    "category": category,
                    "source_date": "2024-01-01",
                }
            }


def get_pomegranate_chunks() -> List[Dict[str, Any]]:
    dadam_path = os.path.join(TRANSCRIPTS_DIR, "bagayat_dadam_ni_kheti.txt")
    chunks = []
    if not os.path.exists(dadam_path):
        return chunks

    with open(dadam_path, "r", encoding="utf-8", errors="ignore") as f:
        dadam_text = f.read()

    chunk_size = 700
    overlap = 120
    dadam_pages = re.split(r"--- પાન \d+ ---", dadam_text)
    for pg_idx, pg_txt in enumerate(dadam_pages):
        pg_txt = pg_txt.strip()
        if len(pg_txt) < 30:
            continue
        sub_chunks = [pg_txt[p:p + chunk_size] for p in range(0, max(1, len(pg_txt)), chunk_size - overlap)]
        for s_idx, sc in enumerate(sub_chunks):
            clean_sc = " ".join(sc.split())
            chunks.append({
                "id": f"dadam_{pg_idx+1}_{s_idx}",
                "text": clean_sc,
                "metadata": {
                    "filename": "દાડમ ની ખેતી.pdf",
                    "pdf_name": "દાડમ ની ખેતી.pdf",
                    "page_number": pg_idx + 1,
                    "subfolder": "Bagayat",
                    "source_name": "દાડમ ની ખેતી (Pomegranate Cultivation)",
                    "source_url": "https://doh.gujarat.gov.in",
                    "category": "Horticulture Schemes",
                    "source_date": "2024-01-01"
                }
            })
    return chunks


def get_standalone_chunks() -> List[Dict[str, Any]]:
    chunks = []
    chunk_size = 700
    overlap = 120
    for fname, title, pdf_ref, url, cat, subf in STANDALONE_RAW:
        fpath = os.path.join(TRANSCRIPTS_DIR, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            t = f.read().strip()
        if not t:
            continue

        sub_chunks = [t[p:p + chunk_size] for p in range(0, max(1, len(t)), chunk_size - overlap)]
        for s_idx, sc_text in enumerate(sub_chunks):
            clean_sc = " ".join(sc_text.split())
            safe_fn = re.sub(r"[^\w]", "_", fname)[:18]
            chunks.append({
                "id": f"std_{safe_fn}_{s_idx}",
                "text": clean_sc,
                "metadata": {
                    "filename": pdf_ref,
                    "pdf_name": pdf_ref,
                    "page_number": s_idx + 1,
                    "subfolder": subf,
                    "source_name": title,
                    "source_url": url,
                    "category": cat,
                    "source_date": "2024-01-01"
                }
            })
    return chunks


def upsert_batch(vector_store, batch: List[Dict[str, Any]]):
    if not batch:
        return
    ids = [c["id"] for c in batch]
    texts = [c["text"] for c in batch]
    metadatas = [c["metadata"] for c in batch]
    embeddings = vector_store.embed_texts(texts)

    vector_store.collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )


def main():
    print("=" * 65)
    print("KHETGPT - STREAMING KNOWLEDGE BASE RE-INDEXING")
    print("=" * 65)

    vector_store = VectorStore.get_instance()
    initial_count = vector_store.count()
    logger.info(f"ChromaDB initial count: {initial_count}")

    # Fetch existing IDs to avoid duplicate work and enable resume
    try:
        existing_records = vector_store.collection.get(include=[])
        existing_ids = set(existing_records["ids"]) if existing_records else set()
    except Exception:
        existing_ids = set()
    logger.info(f"Found {len(existing_ids)} already indexed chunks in collection.")

    batch_size = 12
    total_indexed = 0
    folder_stats = {}
    doc_stats = set()
    t_start = time.time()

    # 1. First, Index Pomegranate (Bagayat) & Standalone Guides
    priority_chunks = [c for c in (get_pomegranate_chunks() + get_standalone_chunks()) if c["id"] not in existing_ids]
    if priority_chunks:
        logger.info(f"Indexing {len(priority_chunks)} priority Pomegranate & summary chunks...")
        for i in range(0, len(priority_chunks), batch_size):
            sub = priority_chunks[i:i + batch_size]
            upsert_batch(vector_store, sub)
            total_indexed += len(sub)
            for c in sub:
                sf = c["metadata"]["subfolder"]
                folder_stats[sf] = folder_stats.get(sf, 0) + 1
                doc_stats.add(c["metadata"]["filename"])
                existing_ids.add(c["id"])
            gc.collect()

    # 2. Stream and Index Each Major Subject Source File
    for raw_file, url, cat, subf in STREAM_SOURCES:
        logger.info(f"\nProcessing domain: {subf} ({raw_file})...")
        file_chunks_buffer = []
        file_count = 0

        for chunk in stream_chunks_from_file(raw_file, url, cat, subf, max_pages=200):
            if chunk["id"] in existing_ids:
                continue

            file_chunks_buffer.append(chunk)
            if len(file_chunks_buffer) >= batch_size:
                upsert_batch(vector_store, file_chunks_buffer)
                file_count += len(file_chunks_buffer)
                total_indexed += len(file_chunks_buffer)
                for c in file_chunks_buffer:
                    folder_stats[c["metadata"]["subfolder"]] = folder_stats.get(c["metadata"]["subfolder"], 0) + 1
                    doc_stats.add(c["metadata"]["filename"])
                    existing_ids.add(c["id"])
                file_chunks_buffer = []
                gc.collect()
                if file_count % 120 == 0:
                    rate = total_indexed / max(0.1, time.time() - t_start)
                    logger.info(f"  [{subf}] Indexed {file_count} new chunks... (Total Added: {total_indexed}, Rate: {rate:.1f} chunks/sec)")

        # Flush any remaining chunks for this file
        if file_chunks_buffer:
            upsert_batch(vector_store, file_chunks_buffer)
            file_count += len(file_chunks_buffer)
            total_indexed += len(file_chunks_buffer)
            for c in file_chunks_buffer:
                folder_stats[c["metadata"]["subfolder"]] = folder_stats.get(c["metadata"]["subfolder"], 0) + 1
                doc_stats.add(c["metadata"]["filename"])
                existing_ids.add(c["id"])
            file_chunks_buffer = []
            gc.collect()

        logger.info(f"Completed {subf}: {file_count} new chunks indexed.")
        gc.collect()

    elapsed = time.time() - t_start
    final_count = vector_store.count()

    print("\n" + "=" * 65)
    print("RE-INDEXING SUMMARY:")
    print(f"  New Chunks Upserted:       {total_indexed}")
    print(f"  ChromaDB Total Chunks:     {final_count}")
    print(f"  Total Unique Documents:    {len(doc_stats)}")
    print(f"  Total Elapsed Time:        {elapsed:.2f} seconds ({total_indexed / max(1, elapsed):.1f} chunks/sec)")
    print("\nBreakdown by Subject Directory:")
    for fld, cnt in sorted(folder_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {fld:25}: {cnt:5d} chunks")
    print("=" * 65)


if __name__ == "__main__":
    main()
