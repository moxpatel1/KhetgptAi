"""
Crop Disease Scan Request/Response Schemas
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class CandidateClass(BaseModel):
    raw_name: str
    crop: str
    disease: str
    confidence: float

class TreatmentAdvisory(BaseModel):
    crop_name: str
    disease_name: str
    symptoms: str
    biological_control: str
    chemical_control: str
    precautions: str
    preventive_measures: str
    official_contact: str

class DiseaseScanResponse(BaseModel):
    success: bool
    raw_class: Optional[str] = None
    crop: Optional[str] = None
    crop_en: Optional[str] = None
    crop_confidence: Optional[float] = None
    disease: Optional[str] = None
    disease_confidence: Optional[float] = None
    is_healthy: Optional[bool] = False
    confidence: Optional[float] = None
    confidence_percentage: Optional[float] = None
    confidence_level: Optional[str] = None
    is_uncertain: Optional[bool] = False
    uncertainty_explanation: Optional[str] = None
    top_candidates: List[CandidateClass] = []
    treatment_advisory: Optional[TreatmentAdvisory] = None
    language: str = "en"
    error: Optional[str] = None

