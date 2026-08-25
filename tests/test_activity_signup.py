from src.app import activities


def test_signup_adds_new_participant(client):
    email = "new.student@mergington.edu"

    response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown%20Club/signup?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(client):
    existing = activities["Chess Club"]["participants"][0]

    response = client.post(f"/activities/Chess%20Club/signup?email={existing}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_missing_email_returns_422(client):
    response = client.post("/activities/Chess%20Club/signup")

    assert response.status_code == 422


def test_signup_invalid_email_returns_422(client):
    response = client.post("/activities/Chess%20Club/signup?email=not-an-email")

    assert response.status_code == 422


def test_signup_full_activity_returns_400(client):
    club = activities["Chess Club"]

    club["participants"] = [f"student{i}@mergington.edu" for i in range(club["max_participants"])]

    response = client.post("/activities/Chess%20Club/signup?email=extra.student@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
