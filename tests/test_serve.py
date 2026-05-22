import pytest
from fastapi.testclient import TestClient

# Bypass Ray Serve Pickling Bug during tests
import ray.serve
ray.serve.ingress = lambda app: lambda cls: cls
ray.serve.deployment = lambda *args, **kwargs: lambda cls: cls

from madewithml.serve import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200

def test_predict_validation_error():
    bad_payload = {"title": "My Machine Learning Project"}
    response = client.post("/predict/", json=bad_payload)
    assert response.status_code == 422