from src.app import activities


def test_unregister_removes_participant(client):
    existing = activities["Chess Club"]["participants"][0]

    response = client.delete(f"/activities/Chess%20Club/signup?email={existing}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {existing} from Chess Club"
    assert existing not in activities["Chess Club"]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete("/activities/Unknown%20Club/signup?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    response = client.delete("/activities/Chess%20Club/signup?email=missing@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in activity"


def test_unregister_missing_email_returns_422(client):
    response = client.delete("/activities/Chess%20Club/signup")

    assert response.status_code == 422


def test_unregister_invalid_email_returns_422(client):
    response = client.delete("/activities/Chess%20Club/signup?email=bad-email")

    assert response.status_code == 422
