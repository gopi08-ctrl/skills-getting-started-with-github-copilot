from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_root_redirect_returns_index():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Mergington High School" in resp.text


def test_get_activities_contains_expected_activity():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Art Studio"
    email = "tester@example.com"

    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should return 400
    resp_dup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp_dup.status_code == 400

    # Unregister
    resp_un = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert resp_un.status_code == 200
    assert email not in activities[activity]["participants"]


def test_nonexistent_activity_returns_404():
    resp = client.get("/activities/DoesNotExist")
    # Accessing a non-existing activity via the listing path should simply return 404
    # But /activities itself exists; here we exercise signup on a missing activity
    resp_signup = client.post(f"/activities/NoSuchActivity/signup", params={"email": "a@b.com"})
    assert resp_signup.status_code == 404
