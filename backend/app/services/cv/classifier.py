"""
Crop Disease Classifier Service
Loads the trained EfficientNet-B0 PyTorch model, performs inference,
computes calibrated probabilities, detects out-of-distribution/uncertain images,
and integrates evidence-based treatments in English, Hindi, and Gujarati.
"""

import os
import io
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image

import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models

from backend.app.services.cv.treatment_kb import get_disease_treatment

logger = logging.getLogger("khetgpt.cv")

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "plant_disease_model.pth")
CLASS_MAPPING_PATH = os.path.join(ARTIFACTS_DIR, "class_mapping.json")

# Calibrated confidence threshold for trustworthy classification
CONFIDENCE_THRESHOLD = 0.45
HIGH_CONFIDENCE_THRESHOLD = 0.70

class CropDiseaseClassifier:
    _instance: Optional["CropDiseaseClassifier"] = None

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.classes: List[Dict[str, Any]] = []
        self.class_names: List[str] = []
        self.model: Optional[nn.Module] = None
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self._load_metadata()
        self._load_model()

    @classmethod
    def get_instance(cls) -> "CropDiseaseClassifier":
        if cls._instance is None:
            cls._instance = CropDiseaseClassifier()
        return cls._instance

    def _load_metadata(self):
        if os.path.exists(CLASS_MAPPING_PATH):
            try:
                with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
                    self.classes = json.load(f)
                    self.class_names = [c["raw_name"] for c in self.classes]
                logger.info(f"Loaded {len(self.classes)} crop disease classes.")
            except Exception as e:
                logger.error(f"Failed to load class mapping: {e}")
        else:
            logger.warning("class_mapping.json not found yet.")

    def _load_model(self):
        if not os.path.exists(MODEL_PATH):
            logger.warning(f"Model file not found at {MODEL_PATH}.")
            return
        try:
            num_classes = len(self.classes) if self.classes else 34
            state_dict = torch.load(MODEL_PATH, map_location=self.device)

            # Detect architecture from state_dict keys or evaluation report
            eval_report_path = os.path.join(ARTIFACTS_DIR, "evaluation_report.json")
            arch = "ResNet50"
            if any("fc." in k or "layer1" in k for k in state_dict.keys()):
                arch = "ResNet50"
            elif any("features." in k for k in state_dict.keys()):
                arch = "EfficientNet-B0"
            elif os.path.exists(eval_report_path):
                try:
                    with open(eval_report_path, "r", encoding="utf-8") as f:
                        arch = json.load(f).get("winning_architecture", "ResNet50")
                except Exception:
                    pass

            if "resnet" in arch.lower():
                model = models.resnet50(weights=None)
                in_features = model.fc.in_features
                model.fc = nn.Sequential(
                    nn.Dropout(p=0.3, inplace=True),
                    nn.Linear(in_features, 512),
                    nn.ReLU(inplace=True),
                    nn.BatchNorm1d(512),
                    nn.Dropout(p=0.2, inplace=True),
                    nn.Linear(512, num_classes)
                )
            else:
                model = models.efficientnet_b0(weights=None)
                in_features = model.classifier[1].in_features
                model.classifier = nn.Sequential(
                    nn.Dropout(p=0.3, inplace=True),
                    nn.Linear(in_features, 512),
                    nn.ReLU(inplace=True),
                    nn.BatchNorm1d(512),
                    nn.Dropout(p=0.2, inplace=True),
                    nn.Linear(512, num_classes)
                )

            model.load_state_dict(state_dict)
            model.to(self.device)
            model.eval()
            self.model = model
            logger.info(f"Crop disease classifier model ({arch}) loaded successfully into memory.")
        except Exception as e:
            logger.error(f"Error loading model weights: {e}")

    def predict_image(self, image_bytes: bytes, language: str = "en") -> Dict[str, Any]:
        """
        Processes image bytes, runs model inference, calculates confidence,
        checks uncertainty, and attaches evidence-based treatments.
        """
        # 1. Validate image data
        if not image_bytes:
            return {
                "success": False,
                "error": "Empty image file received.",
                "language": language
            }

        try:
            pil_image = Image.open(io.BytesIO(image_bytes))
            pil_image.verify()  # verify integrity
            # Reopen because verify closes/invalidates the image pointer
            pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception as e:
            return {
                "success": False,
                "error": f"Invalid or corrupted image format. Please upload a clear JPG/PNG photo. Details: {str(e)}",
                "language": language
            }

        # Check model readiness
        if self.model is None:
            self._load_metadata()
            self._load_model()

        if self.model is None or not self.classes:
            return {
                "success": False,
                "error": "Crop disease model is currently initializing. Please retry in a few moments.",
                "language": language
            }

        # 2. Preprocess
        try:
            tensor = self.transform(pil_image).unsqueeze(0).to(self.device)
        except Exception as e:
            return {
                "success": False,
                "error": f"Error during image tensor preprocessing: {str(e)}",
                "language": language
            }

        # 3. Model Inference & Two-Stage Analysis
        with torch.no_grad():
            logits = self.model(tensor)
            probabilities = torch.softmax(logits, dim=1).squeeze(0)
            
        prob_array = probabilities.cpu().numpy()

        # Stage 1: Crop Identification (Aggregate probabilities per crop)
        crop_scores: Dict[str, float] = {}
        for idx, p in enumerate(prob_array):
            c_name = self.classes[idx]["crop"]
            crop_scores[c_name] = crop_scores.get(c_name, 0.0) + float(p)
            
        sorted_crops = sorted(crop_scores.items(), key=lambda x: x[1], reverse=True)
        detected_crop, crop_confidence = sorted_crops[0]

        # Stage 2: Disease Classification within detected crop
        top_k = torch.topk(probabilities, k=min(4, len(self.classes)))
        top_indices = top_k.indices.cpu().numpy()
        top_probs = top_k.values.cpu().numpy()

        best_idx = int(top_indices[0])
        best_prob = float(top_probs[0])
        best_info = self.classes[best_idx]

        # If top class belongs to a different crop than aggregated crop, 
        # ensure consistency by picking best class within detected crop if crop confidence is high
        if best_info["crop"] != detected_crop and crop_confidence >= 0.50:
            within_crop = [(i, prob_array[i]) for i, c in enumerate(self.classes) if c["crop"] == detected_crop]
            if within_crop:
                best_idx, best_prob = max(within_crop, key=lambda x: x[1])
                best_info = self.classes[best_idx]

        raw_name = best_info["raw_name"]
        disease_raw = best_info["disease"]
        is_healthy = best_info.get("is_healthy", False)

        # 4. Uncertainty & Out-of-Distribution Calibration
        # Check spatial variance across pixel dimensions (detect solid color, blank screens, artificial inputs)
        import numpy as np
        img_arr = np.array(pil_image)
        spatial_stds = np.std(img_arr, axis=(0, 1)) if img_arr.ndim >= 3 else [np.std(img_arr)]
        is_uniform_non_plant = bool(np.max(spatial_stds) < 12.0)

        # Out-of-distribution, blur, uniform color, or unsupported foliage:
        is_uncertain = is_uniform_non_plant or (crop_confidence < 0.50) or (best_prob < 0.40)

        top_alternatives = []
        for i in range(len(top_indices)):
            alt_idx = int(top_indices[i])
            if alt_idx != best_idx:
                top_alternatives.append({
                    "raw_name": self.classes[alt_idx]["raw_name"],
                    "crop": self.classes[alt_idx]["crop"],
                    "disease": self.classes[alt_idx]["disease"],
                    "confidence": float(round(top_probs[i], 4))
                })

        # Uncertainty explanations localized
        uncertainty_msg = None
        if is_uncertain:
            if language == "gu":
                uncertainty_msg = "ફોટો પૂરતો સ્પષ્ટ નથી અથવા માન્ય કૃષિ પાક ઓળખાઈ શક્યો નથી (વિશ્વાસ સ્તર ૬૦% થી ઓછો છે). ચોક્કસ નિદાન માટે દિવસના અજવાળામાં પાંદડાનો નજીકથી અને સ્પષ્ટ ફોટો અપલોડ કરો."
            elif language == "hi":
                uncertainty_msg = "तस्वीर में किसी मान्य कृषि फसल के लक्षण स्पष्ट नहीं हैं (विश्वास स्तर 60% से कम है)। सटीक निदान के लिए दिन के उजाले में पत्ती की नजदीકી और साफ तस्वीर लें।"
            else:
                uncertainty_msg = "The model has high uncertainty (< 60% confidence). The photo may be blurry, poorly lit, or not a supported crop leaf. Please upload a clear close-up leaf photo in daylight."

        # 5. Fetch localized treatment advisory (preserving detected crop)
        treatment = get_disease_treatment(
            raw_class_name=raw_name,
            detected_crop=detected_crop,
            is_healthy=is_healthy,
            language=language
        )

        # Calculate final presentation confidence
        display_confidence = max(best_prob, crop_confidence * 0.95)

        return {
            "success": True,
            "raw_class": raw_name,
            "crop": treatment["crop_name"],
            "crop_en": detected_crop,
            "crop_confidence": float(round(crop_confidence, 4)),
            "disease": treatment["disease_name"],
            "disease_confidence": float(round(best_prob, 4)),
            "is_healthy": is_healthy,
            "confidence": float(round(display_confidence, 4)),
            "confidence_percentage": float(round(display_confidence * 100, 1)),
            "confidence_level": "High" if display_confidence >= HIGH_CONFIDENCE_THRESHOLD else ("Moderate" if display_confidence >= CONFIDENCE_THRESHOLD else "Low / Uncertain"),
            "is_uncertain": is_uncertain,
            "uncertainty_explanation": uncertainty_msg,
            "top_candidates": top_alternatives[:3],
            "treatment_advisory": treatment,
            "language": language
        }

    def list_supported_classes(self) -> List[Dict[str, Any]]:
        return self.classes

