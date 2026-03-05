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
