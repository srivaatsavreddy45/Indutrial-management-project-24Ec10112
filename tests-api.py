from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_predict():
    response = client.post("/predict", json={
        "sku": "A101",
        "inventory_level": 50,
        "historical_sales": [10, 12, 15]
    })

    assert response.status_code == 200
    assert "forecast_value" in response.json()