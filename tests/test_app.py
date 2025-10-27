import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

def test_root_endpoint(client: TestClient):
    """Test that root endpoint serves the index.html file"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_get_activities(client: TestClient):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    # Verify some default activities exist
    assert "Chess Club" in response.json()
    assert "Programming Class" in response.json()

def test_signup_new_participant(client: TestClient):
    """Test signing up a new participant"""
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Ensure the student isn't already registered
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert "Signed up" in response.json()["message"]

def test_signup_duplicate_participant(client: TestClient):
    """Test that a student cannot sign up twice"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Using an email we know exists
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity(client: TestClient):
    """Test signing up for an activity that doesn't exist"""
    response = client.post("/activities/NonexistentClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_participant(client: TestClient):
    """Test unregistering a participant"""
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"  # Using an email we know exists
    
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert "Unregistered" in response.json()["message"]

def test_unregister_nonregistered_participant(client: TestClient):
    """Test unregistering a participant who isn't registered"""
    activity_name = "Chess Club"
    email = "nonexistent@mergington.edu"
    
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]

def test_unregister_from_nonexistent_activity(client: TestClient):
    """Test unregistering from an activity that doesn't exist"""
    response = client.delete("/activities/NonexistentClub/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_activity_data_structure(client: TestClient):
    """Test the structure of activity data"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, details in activities.items():
        assert isinstance(activity_name, str)
        assert isinstance(details, dict)
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)
        assert isinstance(details["max_participants"], int)