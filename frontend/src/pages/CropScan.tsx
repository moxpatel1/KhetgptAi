import React, { useState, useRef } from 'react';
import { 
  Camera, Upload, AlertTriangle, CheckCircle, ShieldAlert, Sparkles, 
  RotateCcw, ChevronDown, ChevronUp, Leaf, FlaskConical, Bug, ShieldCheck, PhoneCall
} from 'lucide-react';
import { type Language, translations } from '../i18n/translations';

interface CropScanProps {
  language: Language;
}

interface TopCandidate {
  raw_name: string;
  crop: string;
  disease: string;
  confidence: number;
}

interface TreatmentAdvisory {
  crop_name: string;
  disease_name: string;
  symptoms: string;
  biological_control: string;
  chemical_control: string;
  precautions: string;
  preventive_measures: string;
  official_contact: string;
}

interface ScanResult {
  success: boolean;
  crop: string;
  disease: string;
  is_healthy: boolean;
  confidence: number;
  confidence_percentage: number;
  confidence_level: string;
  is_uncertain: boolean;
  uncertainty_explanation?: string;
  top_candidates: TopCandidate[];
  treatment_advisory: TreatmentAdvisory;
  error?: string;
}

const API_BASE = import.meta.env.VITE_API_URL || (typeof window !== 'undefined' && window.location.origin.includes('localhost') ? 'http://localhost:8000' : '');

export const CropScan: React.FC<CropScanProps> = ({ language }) => {
  const t = translations[language];
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ScanResult | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Accordion active sections
  const [expandedSection, setExpandedSection] = useState<'chemical' | 'biological' | 'preventive' | 'symptoms'>('chemical');

  const handleFileSelect = (file: File) => {
    if (!file.type.startsWith('image/')) {
      setErrorMsg('Please upload a valid JPG or PNG image.');
      return;
    }
    if (file.size > 15 * 1024 * 1024) {
      setErrorMsg('File size exceeds 15MB limit.');
      return;
    }

    setErrorMsg(null);
    setResult(null);
    setSelectedImage(file);

    const reader = new FileReader();
    reader.onload = () => {
      setImagePreview(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedImage) return;

    setLoading(true);
    setErrorMsg(null);

    const formData = new FormData();
    formData.append('file', selectedImage);
    formData.append('language', language);

    try {
      const response = await fetch(`${API_BASE}/api/disease/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || 'Server error occurred during scan.');
      }

      const data: ScanResult = await response.json();
      if (!data.success) {
        setErrorMsg(data.error || 'Diagnosis failed. Please try a clearer leaf photo.');
      } else {
        setResult(data);
      }
    } catch (err: any) {
      console.error('Scan error:', err);
      setErrorMsg(err.message || 'Unable to connect to AI server. Please verify backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setImagePreview(null);
    setResult(null);
    setErrorMsg(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Preset real test leaf photographs from validation benchmark
  const loadPresetSample = async (sampleType: string) => {
    setErrorMsg(null);
    setResult(null);
    const sampleMap: Record<string, string> = {
      'tomato_early_blight': 'tomato_early_blight.jpg',
      'tomato_late_blight': 'tomato_late_blight.jpg',
      'tomato_bacterial_spot': 'tomato_bacterial_spot.jpg',
      'tomato_healthy': 'tomato_healthy.jpg',
      'potato_early_blight': 'potato_early_blight.jpg',
      'potato_healthy': 'potato_healthy.jpg',
      'early_blight': 'tomato_early_blight.jpg',
      'late_blight': 'tomato_late_blight.jpg',
      'bacterial_spot': 'tomato_bacterial_spot.jpg',
      'healthy': 'tomato_healthy.jpg'
    };

    const fileName = sampleMap[sampleType] || `${sampleType}.jpg`;
    try {
      const res = await fetch(`/samples/${fileName}`);
      if (!res.ok) throw new Error(`Sample file not found: ${fileName}`);
      const blob = await res.blob();
      const file = new File([blob], fileName, { type: blob.type || 'image/jpeg' });
      handleFileSelect(file);
    } catch (err) {
      console.error('Failed to load sample photo:', err);
      setErrorMsg(`Could not load real sample ${fileName}. Please upload a photograph.`);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-16">
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto">
        <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-green-100 text-green-800 text-xs font-bold uppercase tracking-wide mb-3">
          <Leaf className="w-3.5 h-3.5" />
          <span>Real AI Diagnostics</span>
        </div>
        <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight sm:text-4xl">
          {t.scanTitle}
        </h1>
        <p className="mt-2 text-sm sm:text-base text-gray-600">
          {t.scanSubtitle}
        </p>
      </div>

      {/* Preset Quick Samples (Testing helper with real leaf photographs) */}
      <div className="bg-white rounded-2xl p-4 border border-gray-200 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs">
        <span className="font-semibold text-gray-700 flex items-center">
          <Sparkles className="w-4 h-4 text-amber-500 mr-1.5" />
          Test with Real Leaf Photos:
        </span>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => loadPresetSample('tomato_early_blight')}
            className="px-2.5 py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-800 rounded-lg font-medium border border-amber-200 transition-colors"
          >
            Tomato Early Blight
          </button>
          <button
            onClick={() => loadPresetSample('tomato_late_blight')}
            className="px-2.5 py-1.5 bg-red-50 hover:bg-red-100 text-red-800 rounded-lg font-medium border border-red-200 transition-colors"
          >
            Tomato Late Blight
          </button>
          <button
            onClick={() => loadPresetSample('tomato_bacterial_spot')}
            className="px-2.5 py-1.5 bg-orange-50 hover:bg-orange-100 text-orange-800 rounded-lg font-medium border border-orange-200 transition-colors"
          >
            Tomato Bacterial Spot
          </button>
          <button
            onClick={() => loadPresetSample('tomato_healthy')}
            className="px-2.5 py-1.5 bg-green-50 hover:bg-green-100 text-green-800 rounded-lg font-medium border border-green-200 transition-colors"
          >
            Tomato Healthy
          </button>
          <button
            onClick={() => loadPresetSample('potato_early_blight')}
            className="px-2.5 py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-800 rounded-lg font-medium border border-amber-200 transition-colors"
          >
            Potato Early Blight
          </button>
          <button
            onClick={() => loadPresetSample('potato_healthy')}
            className="px-2.5 py-1.5 bg-green-50 hover:bg-green-100 text-green-800 rounded-lg font-medium border border-green-200 transition-colors"
          >
            Potato Healthy
          </button>
        </div>
      </div>

      {/* Upload & Preview Card */}
      {!result && (
        <div className="bg-white rounded-3xl p-6 sm:p-8 border-2 border-dashed border-gray-300 shadow-sm hover:border-green-500 transition-colors">
          <input
            type="file"
            ref={fileInputRef}
            onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
            accept="image/*"
            className="hidden"
          />

          {!imagePreview ? (
            <div 
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className="flex flex-col items-center justify-center py-10 cursor-pointer text-center"
            >
              <div className="w-16 h-16 rounded-2xl bg-green-50 text-green-600 flex items-center justify-center mb-4 shadow-inner">
                <Upload className="w-8 h-8" />
              </div>
              <h3 className="text-lg font-bold text-gray-900 mb-1">
                {t.scanUploadPrompt}
              </h3>
              <p className="text-xs text-gray-500 mb-6">
                {t.scanUploadHint}
              </p>
              <div className="flex flex-wrap gap-3 justify-center">
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    fileInputRef.current?.click();
                  }}
                  className="px-5 py-2.5 bg-green-600 hover:bg-green-700 text-white font-bold rounded-xl text-sm shadow-md transition-colors"
                >
                  {t.scanUploadBtn}
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="relative rounded-2xl overflow-hidden max-h-96 bg-gray-900 flex items-center justify-center">
                <img
                  src={imagePreview}
                  alt="Selected Leaf Preview"
                  className="max-h-96 w-auto object-contain"
                />
                <button
                  onClick={handleReset}
                  className="absolute top-3 right-3 p-2 bg-black/60 hover:bg-black/80 text-white rounded-full backdrop-blur-sm transition-colors"
                  title="Remove image"
                >
                  <RotateCcw className="w-4 h-4" />
                </button>
              </div>

              <div className="flex justify-center gap-4">
                <button
                  onClick={handleReset}
                  className="px-5 py-2.5 border border-gray-300 text-gray-700 font-bold rounded-xl text-sm hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleAnalyze}
                  disabled={loading}
                  className="flex items-center space-x-2 px-8 py-3 bg-gradient-to-r from-green-600 to-emerald-700 hover:from-green-700 hover:to-emerald-800 text-white font-bold rounded-xl text-sm shadow-lg transition-all disabled:opacity-50"
                >
                  {loading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      <span>{t.scanAnalyzing}</span>
                    </>
                  ) : (
                    <>
                      <Camera className="w-4 h-4" />
                      <span>Diagnose Now</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Error Message */}
      {errorMsg && (
        <div className="p-4 rounded-2xl bg-red-50 border border-red-200 text-red-800 flex items-start space-x-3 text-sm">
          <AlertTriangle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <span className="font-bold">Error: </span>
            <span>{errorMsg}</span>
          </div>
        </div>
      )}

      {/* Diagnostic Results Presentation */}
      {result && (
        <div className="space-y-6">
          {/* Main Result Header Card */}
          <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-md">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-6 border-b border-gray-100 gap-4">
              <div className="flex items-center space-x-4">
                <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-white shadow-md ${
                  result.is_healthy ? 'bg-green-600' : 'bg-amber-600'
                }`}>
                  {result.is_healthy ? <CheckCircle className="w-7 h-7" /> : <Bug className="w-7 h-7" />}
                </div>
                <div>
                  <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">
                    {t.scanResultTitle}
                  </span>
                  <h2 className="text-2xl font-black text-gray-900 leading-tight">
                    {result.disease}
                  </h2>
                  <p className="text-sm font-semibold text-green-700">
                    {t.scanCropLabel} {result.crop}
                  </p>
                </div>
              </div>

              {/* Confidence Badge */}
              <div className="text-right sm:text-right">
                <div className="text-xs font-bold text-gray-500 mb-1">
                  {t.scanConfidenceLabel}
                </div>
                <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-sm font-black bg-green-100 text-green-900">
                  <span>{result.confidence_percentage}%</span>
                  <span className="text-xs font-semibold text-green-700">({result.confidence_level})</span>
                </div>
              </div>
            </div>

            {/* Uncertainty Warning Alert if applicable */}
            {result.is_uncertain && (
              <div className="mt-4 p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-900 flex items-start space-x-3 text-xs sm:text-sm">
                <ShieldAlert className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                <div>
                  <div className="font-bold">{t.scanUncertaintyAlert}</div>
                  {result.uncertainty_explanation && (
                    <p className="mt-1 text-amber-800">{result.uncertainty_explanation}</p>
                  )}
                </div>
              </div>
            )}

            {/* Healthy Leaf Banner */}
            {result.is_healthy && (
              <div className="mt-4 p-4 rounded-2xl bg-green-50 border border-green-200 text-green-900 flex items-center space-x-3 text-sm">
                <ShieldCheck className="w-5 h-5 text-green-600 flex-shrink-0" />
                <span className="font-bold">{t.scanHealthyBanner}</span>
              </div>
            )}

            {/* Structured Treatment Advisory Tabs / Accordions */}
            <div className="mt-6 space-y-4">
              {/* Chemical Controls */}
              <div className="border border-gray-200 rounded-2xl overflow-hidden shadow-sm">
                <button
                  onClick={() => setExpandedSection(expandedSection === 'chemical' ? 'symptoms' : 'chemical')}
                  className="w-full flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100/80 transition-colors text-left"
                >
                  <div className="flex items-center space-x-3">
                    <FlaskConical className="w-5 h-5 text-blue-600" />
                    <span className="font-bold text-gray-900 text-sm sm:text-base">
                      {t.scanChemicalTitle}
                    </span>
                  </div>
                  {expandedSection === 'chemical' ? <ChevronUp className="w-5 h-5 text-gray-500" /> : <ChevronDown className="w-5 h-5 text-gray-500" />}
                </button>
                {expandedSection === 'chemical' && (
                  <div className="p-4 sm:p-5 bg-white space-y-3 text-sm border-t border-gray-100">
                    <p className="text-gray-800 leading-relaxed font-medium">
                      {result.treatment_advisory.chemical_control}
                    </p>
                    <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-red-900 text-xs sm:text-sm flex items-start space-x-2">
                      <AlertTriangle className="w-4 h-4 text-red-600 flex-shrink-0 mt-0.5" />
                      <div>
                        <span className="font-bold">{t.scanPrecautionsTitle}: </span>
                        <span>{result.treatment_advisory.precautions}</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Biological & Organic Controls */}
              <div className="border border-gray-200 rounded-2xl overflow-hidden shadow-sm">
                <button
                  onClick={() => setExpandedSection(expandedSection === 'biological' ? 'symptoms' : 'biological')}
                  className="w-full flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100/80 transition-colors text-left"
                >
                  <div className="flex items-center space-x-3">
                    <Leaf className="w-5 h-5 text-green-600" />
                    <span className="font-bold text-gray-900 text-sm sm:text-base">
                      {t.scanOrganicTitle}
                    </span>
                  </div>
                  {expandedSection === 'biological' ? <ChevronUp className="w-5 h-5 text-gray-500" /> : <ChevronDown className="w-5 h-5 text-gray-500" />}
                </button>
                {expandedSection === 'biological' && (
                  <div className="p-4 sm:p-5 bg-white text-sm border-t border-gray-100 text-gray-800 leading-relaxed font-medium">
                    {result.treatment_advisory.biological_control}
                  </div>
                )}
              </div>

              {/* Preventive Measures */}
              <div className="border border-gray-200 rounded-2xl overflow-hidden shadow-sm">
                <button
                  onClick={() => setExpandedSection(expandedSection === 'preventive' ? 'symptoms' : 'preventive')}
                  className="w-full flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100/80 transition-colors text-left"
                >
                  <div className="flex items-center space-x-3">
                    <ShieldCheck className="w-5 h-5 text-emerald-600" />
                    <span className="font-bold text-gray-900 text-sm sm:text-base">
                      {t.scanPreventiveTitle}
                    </span>
                  </div>
                  {expandedSection === 'preventive' ? <ChevronUp className="w-5 h-5 text-gray-500" /> : <ChevronDown className="w-5 h-5 text-gray-500" />}
                </button>
                {expandedSection === 'preventive' && (
                  <div className="p-4 sm:p-5 bg-white text-sm border-t border-gray-100 text-gray-800 leading-relaxed font-medium">
                    {result.treatment_advisory.preventive_measures}
                  </div>
                )}
              </div>

              {/* Symptoms Overview */}
              <div className="border border-gray-200 rounded-2xl overflow-hidden shadow-sm">
                <button
                  onClick={() => setExpandedSection(expandedSection === 'symptoms' ? 'chemical' : 'symptoms')}
                  className="w-full flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100/80 transition-colors text-left"
                >
                  <div className="flex items-center space-x-3">
                    <Bug className="w-5 h-5 text-amber-600" />
                    <span className="font-bold text-gray-900 text-sm sm:text-base">
                      {t.scanSymptomsTitle}
                    </span>
                  </div>
                  {expandedSection === 'symptoms' ? <ChevronUp className="w-5 h-5 text-gray-500" /> : <ChevronDown className="w-5 h-5 text-gray-500" />}
                </button>
                {expandedSection === 'symptoms' && (
                  <div className="p-4 sm:p-5 bg-white text-sm border-t border-gray-100 text-gray-800 leading-relaxed">
                    {result.treatment_advisory.symptoms}
                  </div>
                )}
              </div>
            </div>

            {/* Helpline Advisory Footer */}
            <div className="mt-6 p-4 rounded-xl bg-gray-50 border border-gray-200 flex items-center justify-between text-xs text-gray-600">
              <span className="flex items-center font-medium">
                <PhoneCall className="w-4 h-4 text-green-700 mr-2" />
                {result.treatment_advisory.official_contact}
              </span>
              <button
                onClick={handleReset}
                className="font-bold text-green-700 hover:text-green-800 transition-colors"
              >
                {t.scanResetBtn}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
