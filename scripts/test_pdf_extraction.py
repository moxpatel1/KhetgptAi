import os
import sys

# Force UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

from backend.app.services.rag.extractor import extract_text_from_pdf

folders = ['Bagayat', 'Pashu palan', 'Khetivadi', 'ICAR BOOks']

for fld in folders:
    print(f"\n=== Testing Folder: {fld} ===")
    if not os.path.exists(fld):
        print(f"Directory {fld} does not exist!")
        continue
    pdfs = [f for f in os.listdir(fld) if f.lower().endswith('.pdf')]
    print(f"Total PDFs found: {len(pdfs)}")
    
    for pdf in pdfs[:3]:
        file_path = os.path.join(fld, pdf)
        try:
            pages = extract_text_from_pdf(file_path, max_pages=5, enable_ocr=False)
            content_pages = [p for p in pages if p['has_content']]
            total_chars = sum(p['char_count'] for p in pages)
            print(f"  {pdf}: {len(pages)} pages, {len(content_pages)} with content, total chars = {total_chars}")
            if content_pages:
                print(f"    Sample: {content_pages[0]['text'][:80]}...")
            else:
                print(f"    [EMPTY] No text extracted with pypdf (may need pdfplumber or OCR).")
        except Exception as e:
            print(f"  {pdf}: EXCEPTION: {e}")

