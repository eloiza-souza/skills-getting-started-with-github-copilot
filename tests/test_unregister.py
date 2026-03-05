"""Tests for unregister endpoint (DELETE /activities/{activity_name}/signup)"""
from fastapi.testclient import TestClient
from src import app as application

client = TestClient(application.app)


def test_unregister_from_activity_success_and_not_signed():
    # Arrange
    email = "unregister@mergington.edu"
    activity = "Programming Class"
    client.post(f"/activities/{activity}/signup", params={"email": email})  # ensure we can unregister

    # Act - successful unregister
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert success
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]

    # Act - try unregistering again
    response2 = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert failure path
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Student not signed up for this activity"


def test_unregister_from_nonexistent_activity():
    # Arrange
    url = "/activities/NoSuch/signup"
    params = {"email": "a@b.com"}

    # Act
    response = client.delete(url, params=params)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_email_from_participants():
    # Arrange
    activity = "Music Ensemble"
    email = "unregister_test@mergington.edu"
    
    # First signup
    client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Verify email was added
    participants_before = client.get("/activities").json()[activity]["participants"]
    assert email in participants_before

    # Act - unregister
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    
    # Verify email was removed
    participants_after = client.get("/activities").json()[activity]["participants"]
    assert email not in participants_after
    assert len(participants_after) == len(participants_before) - 1


def test_unregister_with_empty_email():
    # Arrange
    activity = "Tennis Club"
    email = ""

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert - empty email is not signed up
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"
