"""
Crop Disease Classifier Service
Supports high-speed, low-memory ONNX Runtime inference as primary engine
with PyTorch ResNet-50 as local fallback.
Computes calibrated probabilities, detects out-of-distribution/uncertain images,
and integrates evidence-based treatments in English, Hindi, and Gujarati.
"""

import os
import io
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image
import numpy as np

try:
    import onnxruntime as ort
except ImportError:
    ort = None

from backend.app.services.cv.treatment_kb import get_disease_treatment

logger = logging.getLogger("khetgpt.cv")

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
ONNX_QUANT_MODEL_PATH = os.path.join(ARTIFACTS_DIR, "plant_disease_model_quant.onnx")
ONNX_MODEL_PATH = os.path.join(ARTIFACTS_DIR, "plant_disease_model.onnx")
PYTORCH_MODEL_PATH = os.path.join(ARTIFACTS_DIR, "plant_disease_model.pth")
CLASS_MAPPING_PATH = os.path.join(ARTIFACTS_DIR, "class_mapping.json")

# Calibrated confidence threshold for trustworthy classification
CONFIDENCE_THRESHOLD = 0.45
HIGH_CONFIDENCE_THRESHOLD = 0.70

class CropDiseaseClassifier:
    _instance: Optional["CropDiseaseClassifier"] = None

    def __init__(self):
        self.classes: List[Dict[str, Any]] = []
        self.class_names: List[str] = []
        self.engine: Optional[str] = None
        self.onnx_session: Optional[Any] = None
        self.onnx_input_name: Optional[str] = None
        self.torch_model: Optional[Any] = None
        self.torch_device: Optional[Any] = None
        self.torch_transform: Optional[Any] = None

        self._load_metadata()
        self._load_model()

    @classmethod
    def get_instance(cls) -> "CropDiseaseClassifier":
        if cls._instance is None:
            cls._instance = CropDiseaseClassifier()
        return cls._instance

    @property
    def model(self):
        return self.onnx_session or self.torch_model

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
        # 1. Primary Engine: ONNX Runtime (Ultra-fast, ~35MB RAM, ideal for Render)
        if ort is not None:
            active_onnx = None
            if os.path.exists(ONNX_QUANT_MODEL_PATH):
                active_onnx = ONNX_QUANT_MODEL_PATH
            elif os.path.exists(ONNX_MODEL_PATH):
                active_onnx = ONNX_MODEL_PATH

            if active_onnx:
                try:
                    opts = ort.SessionOptions()
                    opts.intra_op_num_threads = 1
                    opts.inter_op_num_threads = 1
                    opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
                    self.onnx_session = ort.InferenceSession(
                        active_onnx,
                        sess_options=opts,
                        providers=["CPUExecutionProvider"]
                    )
                    self.onnx_input_name = self.onnx_session.get_inputs()[0].name
                    self.engine = "onnx"
                    logger.info(f"Crop disease classifier loaded using ONNX Runtime ({os.path.basename(active_onnx)}).")
                    return
                except Exception as e:
                    logger.warning(f"Failed to load ONNX model ({e}), checking PyTorch fallback...")

        # 2. Secondary Engine: PyTorch ResNet-50 fallback (if available locally)
        if os.path.exists(PYTORCH_MODEL_PATH):
            try:
                import torch
                import torch.nn as nn
                import torchvision.models as models
                import torchvision.transforms as transforms

                self.torch_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                num_classes = len(self.classes) if self.classes else 34
                state_dict = torch.load(PYTORCH_MODEL_PATH, map_location=self.torch_device)

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

                model.load_state_dict(state_dict)
                model.to(self.torch_device)
                model.eval()
                self.torch_model = model
                self.torch_transform = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                ])
                self.engine = "pytorch"
                logger.info("Crop disease classifier loaded using PyTorch ResNet-50.")
                return
            except Exception as e:
                logger.error(f"Error loading PyTorch model weights: {e}")

        logger.warning("No disease model weights found (ONNX or PyTorch).")

    def predict_image(self, image_bytes: bytes, language: str = "en") -> Dict[str, Any]:
        """
        Processes image bytes, runs model inference, calculates confidence,
        checks uncertainty, and attaches evidence-based treatments.
        """
        if not image_bytes:
            return {
                "success": False,
                "error": "Empty image file received.",
                "language": language
            }

        try:
            pil_image = Image.open(io.BytesIO(image_bytes))
            pil_image.verify()
            pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception as e:
            return {
                "success": False,
                "error": f"Invalid or corrupted image format. Please upload a clear JPG/PNG photo. Details: {str(e)}",
                "language": language
            }

        # Ensure model is ready
        if self.engine is None or not self.classes:
            self._load_metadata()
            self._load_model()

        if self.engine is None or not self.classes:
            return {
                "success": False,
                "error": "Crop disease model is initializing. Please retry in a few moments.",
                "language": language
            }

        # Inference via ONNX Engine (Default) or PyTorch (Fallback)
        try:
            if self.engine == "onnx" and self.onnx_session is not None:
                img_resized = pil_image.resize((224, 224), Image.BILINEAR)
                arr = np.array(img_resized, dtype=np.float32) / 255.0
                mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
                std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
                arr = (arr - mean) / std
                tensor_np = np.expand_dims(arr.transpose(2, 0, 1), axis=0)

                logits = self.onnx_session.run(None, {self.onnx_input_name: tensor_np})[0][0]
                exp_logits = np.exp(logits - np.max(logits))
                prob_array = exp_logits / exp_logits.sum()

                top_indices = np.argsort(prob_array)[::-1][:min(4, len(self.classes))]
                top_probs = prob_array[top_indices]

            elif self.engine == "pytorch" and self.torch_model is not None:
                import torch
                tensor = self.torch_transform(pil_image).unsqueeze(0).to(self.torch_device)
                with torch.no_grad():
                    logits = self.torch_model(tensor)
                    probabilities = torch.softmax(logits, dim=1).squeeze(0)
                prob_array = probabilities.cpu().numpy()
                top_k = torch.topk(probabilities, k=min(4, len(self.classes)))
                top_indices = top_k.indices.cpu().numpy()
                top_probs = top_k.values.cpu().numpy()
            else:
                return {
                    "success": False,
                    "error": "Inference engine is not available.",
                    "language": language
                }
        except Exception as e:
            logger.error(f"Inference error: {e}", exc_info=True)
            return {
                "success": False,
                "error": f"Image processing failed: {str(e)}",
                "language": language
            }

        # Stage 1: Crop Identification (Aggregate probabilities per crop)
        crop_scores: Dict[str, float] = {}
        for idx, p in enumerate(prob_array):
            c_name = self.classes[idx]["crop"]
            crop_scores[c_name] = crop_scores.get(c_name, 0.0) + float(p)

        sorted_crops = sorted(crop_scores.items(), key=lambda x: x[1], reverse=True)
        detected_crop, crop_confidence = sorted_crops[0]

        # Stage 2: Disease Classification within detected crop
        best_idx = int(top_indices[0])
        best_prob = float(top_probs[0])
        best_info = self.classes[best_idx]

        # Consistency check: ensure top class matches aggregated crop if crop confidence is strong
        if best_info["crop"] != detected_crop and crop_confidence >= 0.50:
            within_crop = [(i, prob_array[i]) for i, c in enumerate(self.classes) if c["crop"] == detected_crop]
            if within_crop:
                best_idx, best_prob = max(within_crop, key=lambda x: x[1])
                best_info = self.classes[best_idx]

        raw_name = best_info["raw_name"]
        disease_raw = best_info["disease"]
        is_healthy = best_info.get("is_healthy", False)

        # 4. Uncertainty & Out-of-Distribution Calibration
        img_arr = np.array(pil_image)
        spatial_stds = np.std(img_arr, axis=(0, 1)) if img_arr.ndim >= 3 else [np.std(img_arr)]
        is_uniform_non_plant = bool(np.max(spatial_stds) < 12.0)

        # True Out-of-Distribution leaf or non-plant:
        # Neither a strong crop match (< 42%) nor a strong disease match (< 32%)
        is_unsupported_crop = is_uniform_non_plant or (crop_confidence < 0.42 and best_prob < 0.32)
        is_uncertain = is_unsupported_crop or (crop_confidence < 0.50 and best_prob < 0.40)

        top_alternatives = []
        for i in range(len(top_indices)):
            alt_idx = int(top_indices[i])
            if alt_idx != best_idx:
                top_alternatives.append({
                    "raw_name": self.classes[alt_idx]["raw_name"],
                    "crop": self.classes[alt_idx]["crop"],
                    "disease": self.classes[alt_idx]["disease"],
                    "confidence": float(round(float(top_probs[i]), 4))
                })

        # Localized uncertainty explanations
        uncertainty_msg = None
        if is_uncertain:
            if language == "gu":
                uncertainty_msg = (
                    "આ પાંદડાનો ફોટો અમારા ૧૪ માન્ય વિઝ્યુઅલ પાકો (ટામેટા, બટાટા, મકાઈ, મરચાં વગેરે) સાથે મેળ ખાતો નથી અથવા ફોટો પૂરતો સ્પષ્ટ નથી. "
                    "જો આ ગુવાર (Guar / Cluster Bean), ચોળી (Cowpea / Lobia), કપાસ, કે ઘઉંનો પાક હોય, તો તે વિઝ્યુઅલ મોડેલમાં સમાવિષ્ટ નથી. "
                    "ચોક્કસ માર્ગદર્શન માટે કૃપા કરીને KhetGPT AI Chat માં પાકના લક્ષણો જણાવી સત્તાવાર સરકારી દસ્તાવેજોમાંથી સલાહ મેળવો."
                )
            elif language == "hi":
                uncertainty_msg = (
                    "यह पत्ती हमारे 14 प्रशिक्षित फसलों (टमाटर, आलू, मक्का, मिर्च आदि) से मेल नहीं खाती या फोटो पूरी तरह स्पष्ट नहीं है। "
                    "यदि यह ग्वार (Guar), लोबिया (Cowpea), कपास, या गेहूं है, तो यह विजुअल मॉडल में शामिल नहीं है। "
                    "सटीक मार्गदर्शन के लिए कृपया KhetGPT AI Chat में लक्षण पूछें।"
                )
            else:
                uncertainty_msg = (
                    "This leaf photo does not match our 14 trained visual scan crops (Apple, Bell Pepper, Blueberry, Cassava, Cherry, Corn, Grape, Peach, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato) or the photo is unclear. "
                    "If this is Guar (Cluster Bean), Cowpea (Lobia), Cotton, or Wheat, it is outside the visual scan classes. "
                    "Please ask KhetGPT AI Chat with your symptoms to retrieve verified advice from official agricultural documents."
                )

        # 5. Fetch localized treatment advisory
        treatment = get_disease_treatment(
            raw_class_name=raw_name,
            detected_crop=detected_crop,
            is_healthy=is_healthy,
            language=language
        )

        crop_display = treatment["crop_name"]
        disease_display = treatment["disease_name"]
        if is_unsupported_crop:
            if language == "gu":
                crop_display = "અસમર્થિત પાક (દા.ત. ગુવાર/ચોળી)"
                disease_display = "લક્ષણ આધારિત KhetGPT Chat નો ઉપયોગ કરો"
            elif language == "hi":
                crop_display = "असमर्थित फसल (उदा. ग्वार/लोबिया)"
                disease_display = "लक्षण आधारित KhetGPT Chat का उपयोग करें"
            else:
                crop_display = "Unsupported Crop (e.g. Guar/Cowpea)"
                disease_display = "Consult KhetGPT Chat for symptoms"

        display_confidence = max(best_prob, crop_confidence * 0.95) if not is_unsupported_crop else min(best_prob, 0.40)

        return {
            "success": True,
            "raw_class": raw_name,
            "crop": crop_display,
            "crop_en": detected_crop if not is_unsupported_crop else "Unsupported Crop",
            "crop_confidence": float(round(crop_confidence, 4)),
            "disease": disease_display,
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
