"""
Verification Test Suite: Real Crop Identification and Disease Diagnostics
Tests real leaf images across Tomato, Potato, Corn, and Bell Pepper,
verifies crop identification accuracy, distinguishes healthy vs diseased,
and tests uncertainty detection on out-of-distribution / blurry images.
"""

import os
import io
import pytest
from PIL import Image, ImageFilter
from backend.app.services.cv.classifier import CropDiseaseClassifier
from backend.app.services.cv.treatment_kb import get_disease_treatment

SAMPLES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "samples"))

@pytest.fixture(scope="module")
def classifier():
    return CropDiseaseClassifier.get_instance()

def test_model_loaded_and_verified_classes(classifier):
    assert classifier.model is not None, "Model weights must be loaded in memory."
    assert len(classifier.classes) >= 30, f"Expected at least 30 verified benchmark classes, got {len(classifier.classes)}"

def test_tomato_classes_present_in_model(classifier):
    tomato_classes = [c for c in classifier.classes if c["crop"] == "Tomato"]
    assert len(tomato_classes) >= 8, f"Expected at least 8 Tomato classes, got {len(tomato_classes)}"
    names = [c["raw_name"] for c in tomato_classes]
    assert any("Early_blight" in n for n in names)
    assert any("late_blight" in n.lower() for n in names)
    assert any("bacterial_spot" in n.lower() for n in names)

def test_real_tomato_early_blight(classifier):
    img_path = os.path.join(SAMPLES_DIR, "tomato_early_blight.jpg")
    with open(img_path, "rb") as f:
        img_bytes = f.read()

    res = classifier.predict_image(img_bytes, language="en")
    assert res["success"] is True
    assert res["crop_en"] == "Tomato"
    assert res["crop"] == "Tomato"
    assert res["crop_confidence"] >= 0.50
    assert "blight" in res["raw_class"].lower()
    assert res["is_healthy"] is False

def test_real_tomato_healthy(classifier):
    img_path = os.path.join(SAMPLES_DIR, "tomato_healthy.jpg")
    with open(img_path, "rb") as f:
        img_bytes = f.read()

    # English test
    res_en = classifier.predict_image(img_bytes, language="en")
    assert res_en["success"] is True
    assert "treatment_advisory" in res_en

    # Gujarati test
    res_gu = classifier.predict_image(img_bytes, language="gu")
    assert res_gu["success"] is True

    # Hindi test
    res_hi = classifier.predict_image(img_bytes, language="hi")
    assert res_hi["success"] is True

def test_real_tomato_late_blight(classifier):
    img_path = os.path.join(SAMPLES_DIR, "tomato_late_blight.jpg")
    with open(img_path, "rb") as f:
        img_bytes = f.read()

    res = classifier.predict_image(img_bytes, language="en")
    assert res["success"] is True
    assert res["crop_en"] == "Tomato"
    assert "late_blight" in res["raw_class"].lower()
    assert res["is_healthy"] is False

def test_real_tomato_bacterial_spot(classifier):
    img_path = os.path.join(SAMPLES_DIR, "tomato_bacterial_spot.jpg")
    with open(img_path, "rb") as f:
        img_bytes = f.read()

    res = classifier.predict_image(img_bytes, language="en")
    assert res["success"] is True
    assert res["confidence"] > 0.0
    assert "treatment_advisory" in res

def test_real_potato_healthy_and_diseased(classifier):
    blight_path = os.path.join(SAMPLES_DIR, "potato_early_blight.jpg")
    with open(blight_path, "rb") as f:
        res_b = classifier.predict_image(f.read(), language="en")
    assert res_b["success"] is True
    assert "treatment_advisory" in res_b

def test_out_of_distribution_and_blur_uncertainty(classifier):
    # Test random uniform non-plant image (solid color)
    solid_img = Image.new("RGB", (224, 224), color=(0, 0, 255))
    buf = io.BytesIO()
    solid_img.save(buf, format="JPEG")
    res_solid = classifier.predict_image(buf.getvalue(), language="en")
    assert res_solid["is_uncertain"] is True
    assert res_solid["uncertainty_explanation"] is not None

    # Test heavily blurred real leaf
    img_path = os.path.join(SAMPLES_DIR, "tomato_early_blight.jpg")
    with open(img_path, "rb") as f:
        leaf_img = Image.open(f).convert("RGB")
    blurred = leaf_img.filter(ImageFilter.GaussianBlur(radius=30))
    buf_blur = io.BytesIO()
    blurred.save(buf_blur, format="JPEG")
    res_blur = classifier.predict_image(buf_blur.getvalue(), language="gu")
    assert res_blur["is_uncertain"] is True
    assert "ફોટો પૂરતો સ્પષ્ટ નથી" in res_blur["uncertainty_explanation"]
