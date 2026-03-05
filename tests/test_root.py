"""Tests for the root endpoint (GET /)"""
from fastapi.testclient import TestClient
from src import app as application

client = TestClient(application.app)


def test_root_redirects_to_static():
    # Arrange: nothing to configure; client already exists

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    # fastapi's RedirectResponse will ultimately serve the static file, we just check URL
    assert "<html" in response.text.lower()
