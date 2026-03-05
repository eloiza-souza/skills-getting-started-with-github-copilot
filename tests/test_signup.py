"""Tests for signup endpoint (POST /activities/{activity_name}/signup)"""
from fastapi.testclient import TestClient
from src import app as application

client = TestClient(application.app)


def test_signup_for_activity_success_and_duplicate():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"

    # Act - first signup
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert success
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Act - duplicate attempt
    response2 = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert failure handled
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_nonexistent_activity():
    # Arrange
    url = "/activities/Nonexistent/signup"
    params = {"email": "a@b.com"}

    # Act
    response = client.post(url, params=params)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_with_empty_email():
    # Arrange
    activity = "Chess Club"
    email = ""

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert - empty email should still work in current implementation
    # (no validation on email format is implemented)
    assert response.status_code == 200


def test_signup_with_special_characters_email():
    # Arrange
    activity = "Programming Class"
    email = "student+test@example.com"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert - special chars in email should be accepted
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]


def test_signup_email_added_to_participants():
    # Arrange
    activity = "Art Studio"
    email = "test_participant@mergington.edu"
    
    # Get initial participants count
    activities_response = client.get("/activities")
    initial_count = len(activities_response.json()[activity]["participants"])

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    
    # Verify email was added
    activities_after = client.get("/activities").json()
    assert email in activities_after[activity]["participants"]
    assert len(activities_after[activity]["participants"]) == initial_count + 1
