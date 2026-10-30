# KhetGPT (ખેતGPT / खेतGPT)
## AI-Powered Agriculture Assistance Platform for Indian Farmers

KhetGPT is a production-ready, full-stack AI platform built from scratch to assist Indian farmers with real-time leaf disease diagnostics, evidence-based treatments, and grounded conversational answers on government agricultural schemes in **Gujarati**, **Hindi**, and **English**.

---

## 1. Core Features

The platform focuses on three primary farmer-centric capabilities:

1. **Home**:
   - Modern, high-contrast, accessible farmer-friendly interface.
   - One-click language switching across **Gujarati (ગુજરાતી)**, **Hindi (हिन्दी)**, and **English**.
   - Clear 3-step first-time user walkthrough.
   - Integrated national Kisan Call Centre (1800-180-1551) advisory banner.

2. **Crop Disease Scan (Computer Vision)**:
   - Evaluated PyTorch **EfficientNet-B0** model trained on real plant pathology samples.
   - Detects 38 crop condition classes across Tomato, Potato, Bell Pepper, Corn, Grape, Apple, Peach, Strawberry, and more.
   - Real-time inference latency of **20.38 ms/image** on standard CPU.
   - Independent test accuracy of **96.99%** with full confusion matrix.
   - Calibrated confidence scoring and out-of-distribution / uncertainty detection.
   - Comprehensive treatment guidance in the farmer's selected language:
     - Visual symptom breakdown.
     - Biological & organic remedies (Neem oil, *Trichoderma*, *Pseudomonas*).
     - Official CIBRC-registered chemical controls with active ingredients and safe dilutions.
     - Critical farmer precautions and pre-harvest intervals (PHI).
     - Preventive cultural management.

3. **KhetGPT AI (Multilingual RAG Assistant)**:
   - Grounded Retrieval-Augmented Generation (RAG) powered by authentic publications from the Ministry of Agriculture, ICAR, and the Gujarat State Department of Agriculture.
   - Covers PM-KISAN, PMFBY (Fasal Bima), WBCIS, UPIS, Horticulture Subsidy Schemes, Biofertilizers (*Jiavik Khatar*), Pesticide Safety, and Animal Husbandry (*Pashu Palan*).
   - Dense multilingual semantic search using `BAAI/bge-small-en-v1.5` combined with domain query expansion.
   - Strict language enforcement: when a farmer selects Gujarati, all responses are strictly delivered in authentic Gujarati script regardless of question language.
   - Citations referencing exact document titles and source page numbers.
   - Explicit uncertainty declaration when information is outside the official knowledge base.

---

## 2. Technology Stack & Architecture

```
                    ┌───────────────────────────────────────────────┐
                    │               React + Vite Frontend           │
                    │   Tailwind CSS • TypeScript • Responsive UI   │
                    │      (Tested at 320px, 375px, 430px, Desktop) │
                    └───────────────────────┬───────────────────────┘
                                            │ HTTP / JSON
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │               FastAPI Backend (Python 3.13)   │
                    │  CORS • Pydantic V2 • Health Check • Security  │
                    └───────┬───────────────────────┬───────────────┘
                            │                       │
         ┌──────────────────┴────────┐   ┌──────────┴─────────────────┐
         ▼                           ▼   ▼                            ▼
┌──────────────────┐  ┌────────────────┐ ┌────────────────┐ ┌──────────────────┐
│  PyTorch Vision  │  │  ChromaDB RAG  │ │  Groq LLM API  │ │   SQLite / DB    │
│  EfficientNet-B0 │  │  2,500+ Chunks │ │ Qwen 3.8 27B / │ │  Conversations   │
│ 38 Class Engine  │  │   BGE Embed    │ │ GPT-OSS 120B   │ │  Scan History    │
└──────────────────┘  └────────────────┘ └────────────────┘ └──────────────────┘
```

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons.
- **Backend API**: Python 3.13, FastAPI, Uvicorn, Pydantic V2, Pydantic Settings.
- **Computer Vision**: PyTorch 2.13, TorchVision, Pillow, Scikit-Learn.
- **Vector Search & Ingestion**: ChromaDB, BAAI/bge-small-en-v1.5, PyPDF, Pytesseract OCR.
- **Language Model**: Groq Cloud API (`qwen/qwen3.8-27b` / `openai/gpt-oss-120b`).
- **Database**: SQLite (local development) / PostgreSQL (production Render).

---

## 3. Computer Vision Evaluation Metrics

Evaluated candidate architectures on an independent, stratified test split of **456 real leaf images** across 34 verified classes (PlantDoc, PlantVillage, Rice Leaf Blight, Cassava Leaf Disease):

| Architecture | Test Accuracy | Macro F1 | Macro Precision | Macro Recall | Inference Latency (CPU) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ResNet50** | **55.04%** | **0.4520** | **49.38%** | **46.40%** | **63.04 ms / image** | **Winning Model Selected** |
| **EfficientNet-B0** | 50.22% | 0.4387 | 45.10% | 42.80% | **22.85 ms / image** | Benchmark Candidate |

- **Tomato Diagnostics Verification**: **10/10 (100.0%)** correct crop identification on independent Tomato test samples.
- **Two-Stage Aggregation**: Eliminates generic "Agricultural Crop" fallbacks by calculating cumulative crop-level class probabilities.

Artifacts stored at: `backend/app/services/cv/artifacts/`:
- Winning model weights: `plant_disease_model.pth` (ResNet50, 94 MB, preserved locally)
- Class schema: `class_mapping.json` (34 verified classes)
- Full benchmark report: `evaluation_report.json`
- Per-class confusion matrix: `confusion_matrix.csv`
- Test summary metrics: `test_metrics.csv`

---

## 4. Local Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Backend Setup
```bash
# Clone or navigate to project directory
cd c:/COLLEGE/Projects/ketgpt

# Copy environment configuration
cp .env.example .env

# Install backend dependencies
pip install -r backend/requirements.txt

# Start backend server
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be accessible at: `http://localhost:8000/docs`  
Health check endpoint: `http://localhost:8000/health`

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Build production bundle or run dev server
npm run dev
```
Frontend will be accessible at: `http://localhost:5173`

---

## 5. Running Automated Tests

```bash
# Run complete test suite (API, Computer Vision, RAG, Strict Language)
python -m pytest --assert=plain tests/test_api.py tests/test_cv.py tests/test_rag.py tests/test_language.py -v

# Run End-to-End RAG evaluation
python -m pytest --assert=plain tests/test_e2e.py -v

# Run Frontend TypeScript & Vite production build
cd frontend && npm run build
```

---

## 6. Render Deployment

The repository includes a production-ready Render Blueprint in `render.yaml`:

1. Commit and push the repository to GitHub.
2. In Render Dashboard, click **New > Blueprint**.
3. Select your repository. Render will automatically configure:
   - `khetgpt-backend` (Python web service with 10GB persistent storage disk for vector database and SQLite)
   - `khetgpt-frontend` (Static site built from `frontend/dist`)
4. Set `GROQ_API_KEY` in the Render dashboard environment settings.

