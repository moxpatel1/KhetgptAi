"""
Master Benchmark Runner: Stratified Splits, ResNet50 vs EfficientNet-B0 Training, Evaluation & Tomato Verification
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import logging
from scripts.data_preparation_and_training import scan_and_verify_raw_images
from scripts.train_and_evaluate_models import run_benchmark

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("khetgpt.benchmark_master")

def main():
    logger.info("=== STEP 1: Scanning and Verifying Acquired Raw Datasets ===")
    samples, manifest = scan_and_verify_raw_images()
    logger.info("Total verified images: %d", len(samples))

    # Collect class buckets
    class_names = sorted(list(set(s["class"] for s in samples)))
    logger.info("Total classes: %d", len(class_names))

    # Stratified 70/15/15 splits
    class_to_idx = {c: i for i, c in enumerate(class_names)}
    class_buckets = {c: [] for c in class_names}
    for s in samples:
        class_buckets[s["class"]].append((s["path"], class_to_idx[s["class"]]))

    train_samples, val_samples, test_samples = [], [], []
    for c, items in class_buckets.items():
        n = len(items)
        n_train = max(1, int(n * 0.70))
        n_val = max(1, int(n * 0.15))
        train_samples.extend(items[:n_train])
        val_samples.extend(items[n_train:n_train + n_val])
        test_samples.extend(items[n_train + n_val:])

    logger.info("Dataset Splits: Train=%d, Val=%d, Test=%d", len(train_samples), len(val_samples), len(test_samples))

    # Save class mapping
    class_mapping = []
    for idx, c in enumerate(class_names):
        # Extract crop and disease
        if "___" in c:
            parts = c.split("___")
            crop = parts[0].replace("_", " ")
            disease = parts[1].replace("_", " ")
        else:
            parts = c.split("_")
            crop = parts[0]
            disease = " ".join(parts[1:]) if len(parts) > 1 else "unspecified"

        is_h = "healthy" in c.lower() or "leaf" in disease.lower() and "spot" not in disease.lower() and "blight" not in disease.lower()
        class_mapping.append({
            "class_id": idx,
            "raw_name": c,
            "crop": crop,
            "disease": disease,
            "is_healthy": is_h
        })

    mapping_path = os.path.join("backend", "app", "services", "cv", "artifacts", "class_mapping.json")
    with open(mapping_path, "w", encoding="utf-8") as f:
        json.dump(class_mapping, f, indent=2)
    logger.info("Class mapping saved with %d classes.", len(class_mapping))

    logger.info("=== STEP 2: Training and Evaluating Multi-Model Candidates (EfficientNet-B0 vs ResNet50) ===")
    report = run_benchmark(train_samples, val_samples, test_samples, class_names)
    logger.info("Benchmark complete! Winning architecture: %s", report["winning_architecture"])

    logger.info("=== STEP 3: Tomato Diagnostics & Verification ===")
    from backend.app.services.cv.classifier import CropDiseaseClassifier
    classifier = CropDiseaseClassifier()
    classifier._load_metadata()
    classifier._load_model()

    # Find test samples for Tomato
    tomato_test = [path for path, label in test_samples if "tomato" in class_names[label].lower()]
    logger.info("Found %d Tomato test samples in independent test split.", len(tomato_test))

    passed_tomato = 0
    for path in tomato_test[:5]:
        with open(path, "rb") as fp:
            res = classifier.predict_image(fp.read(), language="en")
            logger.info("Test Image %s -> Crop: %s (Confidence: %.2f%%), Disease: %s",
                        os.path.basename(path), res["crop"], res["confidence_percentage"], res["disease"])
            if "tomato" in res["crop"].lower() or "tomato" in res.get("crop_en", "").lower():
                passed_tomato += 1

    logger.info("Tomato Test Accuracy: %d/%d passed", passed_tomato, min(5, len(tomato_test)))


if __name__ == "__main__":
    main()
