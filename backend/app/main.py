"""
KhetGPT Backend Application Entry Point
FastAPI application with CORS, database lifecycle, and modular routers.
"""

import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.app.core.config import settings
from backend.app.core.database import engine, Base
import backend.app.models.db_models  # Ensure models are registered with Base

# Import Routers
from backend.app.api.health import router as health_router
from backend.app.api.disease import router as disease_router
from backend.app.api.chat import router as chat_router
from backend.app.api.documents import router as documents_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("khetgpt.main")

# Auto-create database tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables initialized successfully.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="KhetGPT - AI-powered agriculture assistance platform for Indian farmers.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Error Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again shortly."}
    )

# Include API Routers
app.include_router(health_router)
app.include_router(disease_router)
app.include_router(chat_router)
app.include_router(documents_router)

# Mount static uploads if exists
UPLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "uploads"))
os.makedirs(UPLOADS_DIR, exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

@app.get("/")
def root():
    return {
        "message": "Welcome to KhetGPT API",
        "description": "AI-powered agriculture assistance for Indian farmers (Gujarati, Hindi, English)",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)

