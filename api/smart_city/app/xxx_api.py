from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_running():
    response = client.get("/")
    assert response.status_code == 200

def test_prediction():
    payload = {
        "traffic_intensity": 0.8,
        "speed_efficiency": 0.3,
        "peak_traffic": 1,
        "weather_impact": 0.5,
        "event_impact": 0.4,
        "brt_pressure": 0.6 
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    assert "probabilities" in data