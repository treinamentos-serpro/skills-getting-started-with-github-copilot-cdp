import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient

from app import app, activities


client = TestClient(app)


def reset_activities():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
    activities["Gym Class"]["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
    activities["Soccer Team"]["participants"] = []
    activities["Basketball Club"]["participants"] = []
    activities["Drama Club"]["participants"] = []
    activities["Art Studio"]["participants"] = []
    activities["Debate Team"]["participants"] = []
    activities["Science Olympiad"]["participants"] = []


def test_cancel_signup_removes_participant():
    reset_activities()
    activities["Chess Club"]["participants"].append("student@mergington.edu")

    response = client.delete("/activities/Chess Club/signup?email=student@mergington.edu")

    assert response.status_code == 200
    assert "student@mergington.edu" not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Removed student@mergington.edu from Chess Club"


def test_signup_duplicate_is_rejected():
    reset_activities()

    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_when_activity_is_full_is_rejected():
    reset_activities()
    activity = activities["Chess Club"]
    activity["participants"] = [f"student{i}@mergington.edu" for i in range(activity["max_participants"])]

    response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")

    assert response.status_code == 400
    assert "full" in response.json()["detail"].lower()
