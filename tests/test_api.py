"""
Automated FastAPI Endpoint Tests
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "KhetGPT" in response.json()["message"]

def test_disease_classes():
    response = client.get("/api/disease/classes")
    assert response.status_code == 200
    data = response.json()
    assert data["total_classes"] == 38
    assert len(data["classes"]) == 38

def test_knowledge_base_stats():
    response = client.get("/api/documents/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_chunks" in data
    assert "total_documents" in data

def test_conversations_list():
    response = client.get("/api/conversations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

