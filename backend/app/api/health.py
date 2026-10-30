"""
Health Check API Endpoint for Render and Uptime Monitoring
"""

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.app.core.database import get_db

router = APIRouter(tags=["Health"])

@router.get("/health")
@router.get("/api/health")
def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy",
        "service": "KhetGPT Backend API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status
    }

