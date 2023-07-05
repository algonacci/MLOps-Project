import pytest
from fastapi.testclient import TestClient

from main import app, TextInput


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": {
            "code": 200,
            "message": "Success fetching the API"
        }
    }


def test_predict_ham(client):
    input_data = {"text": "This is a test email"}
    response = client.post("/predict", json=input_data)
    assert response.status_code == 200
    assert response.json() == {"prediction": "Ham"}


def test_predict_spam(client):
    input_data = {"text": "This is a promotion email to get discount"}
    response = client.post("/predict", json=input_data)
    assert response.status_code == 200
    assert response.json() == {"prediction": "Spam"}


if __name__ == "__main__":
    pytest.main([__file__])
