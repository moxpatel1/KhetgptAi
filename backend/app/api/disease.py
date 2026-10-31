"""
Crop Disease Scan API Router
"""

import json
import os
import logging
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.db_models import DiseaseScan
from backend.app.schemas.disease import DiseaseScanResponse

logger = logging.getLogger("khetgpt.api.disease")
router = APIRouter(prefix="/api/disease", tags=["Crop Disease Scan"])

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
MAX_IMAGE_SIZE = 15 * 1024 * 1024  # 15 MB

@router.post("/predict", response_model=DiseaseScanResponse)
async def predict_crop_disease(
    file: UploadFile = File(...),
    language: str = Form("en"),
    db: Session = Depends(get_db)
):
    """
    Analyzes an uploaded leaf photograph using the trained PyTorch model.
    Returns predicted crop, disease, calibrated confidence, uncertainty alert,
    and verified agricultural treatment guidance localized to Gujarati, Hindi, or English.
    """
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file.content_type}'. Please upload a JPG or PNG image."
        )

    image_bytes = await file.read()
    if len(image_bytes) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 15MB limit. Please upload a compressed leaf photograph."
        )

    from backend.app.services.cv.classifier import CropDiseaseClassifier
    classifier = CropDiseaseClassifier.get_instance()
    result = classifier.predict_image(image_bytes=image_bytes, language=language)

    if not result.get("success", False):
        return DiseaseScanResponse(
            success=False,
            error=result.get("error", "Image analysis failed."),
            language=language
        )

    # Persist scan history
    try:
        scan_record = DiseaseScan(
            crop_name=result.get("crop", "Unknown"),
            disease_name=result.get("disease", "Unknown"),
            raw_class=result.get("raw_class", "Unknown"),
            confidence=result.get("confidence", 0.0),
            is_uncertain=result.get("is_uncertain", False),
            is_healthy=result.get("is_healthy", False),
            language=language,
            treatment_summary=str(result.get("treatment_advisory", {}).get("chemical_control", ""))[:500]
        )
        db.add(scan_record)
        db.commit()
    except Exception as e:
        logger.warning(f"Could not persist disease scan to database: {e}")

    return DiseaseScanResponse(**result)

@router.get("/classes")
def list_supported_classes():
    """Returns all 38 supported crop & disease classes without loading PyTorch."""
    mapping_path = os.path.join(os.path.dirname(__file__), "..", "services", "cv", "artifacts", "class_mapping.json")
    if os.path.exists(mapping_path):
        try:
            with open(mapping_path, "r", encoding="utf-8") as f:
                classes = json.load(f)
            return {
                "total_classes": len(classes),
                "classes": classes
            }
        except Exception as e:
            logger.warning(f"Failed to read class mapping json: {e}")
    from backend.app.services.cv.classifier import CropDiseaseClassifier
    classifier = CropDiseaseClassifier.get_instance()
    return {
        "total_classes": len(classifier.classes),
        "classes": classifier.classes
    }

@router.get("/history")
def get_recent_scans(limit: int = Query(10, le=50), db: Session = Depends(get_db)):
    """Returns recent disease scans performed by farmers."""
    scans = db.query(DiseaseScan).order_by(DiseaseScan.created_at.desc()).limit(limit).all()
    return scans

