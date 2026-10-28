
from fastapi.testclient import TestClient

from src.datapulse.api.main import app

client = TestClient(app)


def test_root_returns_project_information():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["project"] == "DataPulse"


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
