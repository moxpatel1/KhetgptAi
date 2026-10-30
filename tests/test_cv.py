"""
Automated Unit and Integration Tests for Crop Disease CV Pipeline
"""

import os
import io
import pytest
from PIL import Image
from backend.app.services.cv.classifier import CropDiseaseClassifier
from backend.app.services.cv.treatment_kb import get_disease_treatment

def create_synthetic_leaf(color=(46, 125, 50)):
    img = Image.new("RGB", (224, 224), color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def test_classifier_initialization():
    classifier = CropDiseaseClassifier.get_instance()
    assert classifier.model is not None, "Model should be loaded into memory"
    assert len(classifier.classes) == 38, f"Expected 38 classes, got {len(classifier.classes)}"

def test_valid_image_inference():
    classifier = CropDiseaseClassifier.get_instance()
    img_bytes = create_synthetic_leaf()
    
    result = classifier.predict_image(img_bytes, language="en")
    assert result["success"] is True
    assert "crop" in result
    assert "disease" in result
    assert "confidence" in result
    assert result["confidence"] >= 0.0 and result["confidence"] <= 1.0
    assert "treatment_advisory" in result

def test_corrupt_image_rejection():
    classifier = CropDiseaseClassifier.get_instance()
    corrupt_bytes = b"NOT_A_VALID_JPEG_HEADER_12345"
    
    result = classifier.predict_image(corrupt_bytes, language="en")
    assert result["success"] is False
    assert "error" in result

def test_empty_bytes_rejection():
    classifier = CropDiseaseClassifier.get_instance()
    result = classifier.predict_image(b"", language="en")
    assert result["success"] is False

def test_multilingual_treatment_retrieval():
    # Test English
    trt_en = get_disease_treatment("Tomato___Early_blight", language="en")
    assert "Tomato" in trt_en["crop_name"]
    assert "Early Blight" in trt_en["disease_name"]
    assert "1800-180-1551" in trt_en["official_contact"]

    # Test Gujarati
    trt_gu = get_disease_treatment("Tomato___Early_blight", language="gu")
    assert "ટામેટા" in trt_gu["crop_name"]
    assert "અગેતી સુકારો" in trt_gu["disease_name"]

    # Test Hindi
    trt_hi = get_disease_treatment("Tomato___Early_blight", language="hi")
    assert "टमाटर" in trt_hi["crop_name"]
    assert "अगेती झुलसा" in trt_hi["disease_name"]

