import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    """Create a test client for our FastAPI app"""
    return TestClient(app)

@pytest.fixture
def sample_activity():
    """Return a sample activity data structure"""
    return {
        "description": "Test activity description",
        "schedule": "Monday, 3:00 PM - 4:00 PM",
        "max_participants": 10,
        "participants": ["test1@mergington.edu", "test2@mergington.edu"]
    }