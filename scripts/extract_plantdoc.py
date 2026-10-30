"""
Extract and verify PlantDoc dataset with Windows filename sanitization & extended path support
"""

import os
import zipfile
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

zip_path = os.path.abspath("data/raw/plantdoc/PlantDoc.zip")
extract_dir = os.path.abspath("data/raw/plantdoc")
win_extract_dir = f"\\\\?\\{extract_dir}"

logging.info(f"Extracting {zip_path} ({os.path.getsize(zip_path)/(1024*1024):.1f} MB)...")
extracted_count = 0

with zipfile.ZipFile(zip_path, "r") as zf:
    for member in zf.infolist():
        # Sanitize illegal Windows NTFS characters in filename
        parts = member.filename.replace("/", os.sep).split(os.sep)
        clean_parts = []
        for p in parts:
            clean_p = p
            for ch in ['?', '*', ':', '<', '>', '|', '"']:
                clean_p = clean_p.replace(ch, '_')
            clean_parts.append(clean_p)

        norm_fn = os.sep.join(clean_parts)
        target_path = os.path.join(win_extract_dir, norm_fn)

        if member.is_dir():
            os.makedirs(target_path, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            try:
                with zf.open(member) as source, open(target_path, "wb") as target:
                    target.write(source.read())
                extracted_count += 1
            except Exception as e:
                logging.warning(f"Skipping {norm_fn}: {e}")

logging.info(f"PlantDoc zip successfully extracted {extracted_count} files!")
