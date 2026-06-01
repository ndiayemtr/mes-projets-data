# tests/test_api.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_predict_endpoint():
    payload = {
        "traffic_intensity": 0.5,
        "speed_efficiency": 0.7,
        "peak_traffic": 1,
        "weather_impact": 0.2,
        "event_impact": 0.1,
        "brt_pressure": 0.3
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    assert "probabilities" in data