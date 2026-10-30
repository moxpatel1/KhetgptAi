"""
KhetGPT PDF Text Extractor with Scanned Page OCR Fallback
Extracts text page by page, cleans whitespace, preserves tables,
and applies pytesseract OCR for scanned or image-heavy pages.
"""

import os
import hashlib
import logging
from typing import List, Dict, Any, Optional
import pypdf

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None

logger = logging.getLogger("khetgpt.rag.extractor")

def compute_file_hash(filepath: str) -> str:
    """Computes SHA-256 hash to detect duplicates and track document updates."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def extract_text_from_pdf(
    filepath: str,
    max_pages: Optional[int] = None,
    enable_ocr: bool = True
) -> List[Dict[str, Any]]:
    """
    Extracts text page by page.
    Returns a list of dicts:
    [
        {
            "page_number": int (1-based),
            "text": str,
            "char_count": int,
            "is_ocr": bool,
            "has_content": bool
        }, ...
    ]
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"PDF file not found: {filepath}")

    extracted_pages = []
    
    try:
        reader = pypdf.PdfReader(filepath)
        num_pages = len(reader.pages)
        if max_pages:
            num_pages = min(num_pages, max_pages)

        for page_idx in range(num_pages):
            page_num = page_idx + 1
            page = reader.pages[page_idx]
            text = page.extract_text() or ""
            text = text.strip()
            is_ocr = False

            # If page text is very sparse (< 30 characters), attempt OCR if available
            if len(text) < 30 and enable_ocr and pytesseract:
                try:
                    # Check for embedded images on this page
                    for img_obj in page.images:
                        img_bytes = img_obj.data
                        import io
                        img = Image.open(io.BytesIO(img_bytes)).convert("L")
                        ocr_text = pytesseract.image_to_string(img, lang="eng+guj+hin")
                        if len(ocr_text.strip()) > len(text):
                            text = ocr_text.strip()
                            is_ocr = True
                            break
                except Exception as ocr_err:
                    logger.debug(f"OCR skipped for {os.path.basename(filepath)} p.{page_num}: {ocr_err}")

            # Clean extraction artifacts (remove null characters and excessive whitespace)
            clean_text = " ".join(text.split())
            clean_text = clean_text.replace("\x00", "")

            extracted_pages.append({
                "page_number": page_num,
                "text": clean_text,
                "char_count": len(clean_text),
                "is_ocr": is_ocr,
                "has_content": len(clean_text) >= 20
            })

    except Exception as e:
        logger.error(f"Error extracting text from {filepath}: {e}")
        # Try pdfplumber fallback if available
        if pdfplumber:
            try:
                with pdfplumber.open(filepath) as pdf:
                    for i, page in enumerate(pdf.pages):
                        if max_pages and i >= max_pages:
                            break
                        txt = page.extract_text() or ""
                        clean = " ".join(txt.split()).replace("\x00", "")
                        extracted_pages.append({
                            "page_number": i + 1,
                            "text": clean,
                            "char_count": len(clean),
                            "is_ocr": False,
                            "has_content": len(clean) >= 20
                        })
            except Exception as e2:
                logger.error(f"pdfplumber fallback also failed for {filepath}: {e2}")

    return extracted_pages

