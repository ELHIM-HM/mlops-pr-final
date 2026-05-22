import pytest
import requests

# The API is running inside Docker and mapped to port 8000 on the host
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Ensure the deployed root endpoint returns a 200 OK status."""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json()["status-code"] == 200
    assert "environment" in response.json()

def test_predict_validation_error():
    """Ensure the deployed API rejects bad payloads."""
    bad_payload = {"title": "My Machine Learning Project"}
    
    response = requests.post(f"{BASE_URL}/predict/", json=bad_payload)
    
    assert response.status_code == 422