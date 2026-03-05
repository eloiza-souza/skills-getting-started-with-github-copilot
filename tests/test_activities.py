"""Tests for the activities endpoint (GET /activities)"""
from fastapi.testclient import TestClient
from src import app as application

client = TestClient(application.app)


def test_get_activities_returns_dict():
    # Arrange: nothing to configure

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # should contain at least one known activity
    assert "Chess Club" in data


def test_get_activities_returns_all_required_fields():
    # Arrange: nothing to configure

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Verify structure for each activity
    required_fields = {"description", "schedule", "max_participants", "participants"}
    for activity_name, activity_data in data.items():
        assert isinstance(activity_data, dict), f"{activity_name} should be a dict"
        assert required_fields.issubset(activity_data.keys()), \
            f"{activity_name} missing required fields: {required_fields - set(activity_data.keys())}"
        
        # Type validation
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_get_activities_contains_expected_activities():
    # Arrange
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Art Studio", "Music Ensemble", "Debate Team", "Science Club"
    ]

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    for activity in expected_activities:
        assert activity in data, f"Expected activity '{activity}' not found in response"
