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


def test_predict_empty_input(client):
    input_data = {"text": ""}
    response = client.post("/predict", json=input_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Empty input text"}


def test_unsupported_http_method(client):
    response = client.put("/predict")
    assert response.status_code == 405


def test_missing_required_field(client):
    input_data = {"wrong_field": "This is a test"}
    response = client.post("/predict", json=input_data)
    assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__])
