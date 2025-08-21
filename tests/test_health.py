from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """
    Test para el endpoint de health check básico
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["service"] == "FastAPI"

def test_detailed_health_check():
    """
    Test para el endpoint de health check detallado
    """
    response = client.get("/api/v1/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["service"] == "FastAPI"
    assert "checks" in data
    assert data["checks"]["database"] == "ok"
    assert data["checks"]["external_services"] == "ok"
