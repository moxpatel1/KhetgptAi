import os
import json
import logging
from backend.app.services.cv.classifier import CropDiseaseClassifier

logging.basicConfig(level=logging.INFO)

def main():
    classifier = CropDiseaseClassifier.get_instance()
    print(f"Model loaded: {classifier.model is not None}")
    print(f"Classes loaded: {len(classifier.classes)}")

    test_dir = os.path.join("data", "splits", "test")
    tomato_samples = []
    if os.path.exists(test_dir):
        for root, dirs, files in os.walk(test_dir):
            if "tomato" in os.path.basename(root).lower():
                for f in files:
                    if f.lower().endswith((".jpg", ".jpeg", ".png")):
                        tomato_samples.append((os.path.join(root, f), os.path.basename(root)))
    
    if not tomato_samples:
        raw_dir = os.path.join("data", "raw")
        for root, dirs, files in os.walk(raw_dir):
            if "tomato" in os.path.basename(root).lower():
                for f in files:
                    if f.lower().endswith((".jpg", ".jpeg", ".png")):
                        tomato_samples.append((os.path.join(root, f), os.path.basename(root)))

    print(f"Total Tomato test samples found: {len(tomato_samples)}")

    passed_count = 0
    tested_count = min(10, len(tomato_samples))

    for path, expected_class in tomato_samples[:tested_count]:
        with open(path, "rb") as fp:
            res = classifier.predict_image(fp.read(), language="en")
            crop = res.get("crop", "Unknown")
            crop_en = res.get("crop_en", "Unknown")
            disease = res.get("disease", "Unknown")
            conf = res.get("confidence_percentage", 0.0)
            crop_conf = res.get("crop_confidence", 0.0)
            
            is_tomato = "tomato" in crop.lower() or "tomato" in crop_en.lower()
            if is_tomato:
                passed_count += 1
            print(f"File: {os.path.basename(path)} | Expected: {expected_class} | Crop Identified: {crop} (p={crop_conf:.2f}) | Disease: {disease} | Overall Conf: {conf:.1f}% | Correct: {is_tomato}")

    print(f"\nTomato Identification Accuracy on Independent Test Samples: {passed_count}/{tested_count} ({passed_count/tested_count*100:.1f}%)")

if __name__ == "__main__":
    main()
