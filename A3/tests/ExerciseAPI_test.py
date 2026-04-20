# ExerciseAPI_test.py - Verifies all Quiz Game routes are accessible from the Flask server.
# Run with:  python -m pytest A3/tests/ExerciseAPI_test.py -v

import os
import sys

import pytest

# Make the A3 package importable when running from the repo root or from A3/.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app  # noqa: E402


@pytest.fixture
def client():
    """Flask test client with a fresh session per test."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_index_route_serves_page(client):
    """GET / should return the quiz arcade HTML page."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"QUIZ ARCADE" in response.data


def test_categories_route(client):
    """GET /api/categories should return the list of categories."""
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.get_json()
    assert "categories" in data
    assert isinstance(data["categories"], list)
    assert len(data["categories"]) > 0


def test_set_name_valid(client):
    """POST /api/set-name with a valid name should save it."""
    response = client.post("/api/set-name", json={"username": "TestUser"})
    assert response.status_code == 200
    assert response.get_json()["username"] == "TestUser"


def test_set_name_invalid_empty(client):
    """POST /api/set-name with an empty name should return 400."""
    response = client.post("/api/set-name", json={"username": ""})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_set_name_invalid_symbols(client):
    """POST /api/set-name with special characters should return 400."""
    response = client.post("/api/set-name", json={"username": "bad@name!"})
    assert response.status_code == 400


def test_questions_route_valid(client):
    """GET /api/questions with valid params should return questions."""
    response = client.get("/api/questions?category=history&difficulty=easy")
    assert response.status_code == 200
    data = response.get_json()
    assert "questions" in data
    assert isinstance(data["questions"], list)
    if data["questions"]:
        q = data["questions"][0]
        assert "question" in q
        assert "options" in q
        assert "points" in q


def test_questions_route_missing_params(client):
    """GET /api/questions without params should return 400."""
    response = client.get("/api/questions")
    assert response.status_code == 400


def test_questions_route_unknown_category(client):
    """GET /api/questions with an unknown category should return 404."""
    response = client.get("/api/questions?category=not_real&difficulty=easy")
    assert response.status_code == 404


def test_submit_score_without_name(client):
    """POST /api/submit-score before setting a name should return 400."""
    payload = {
        "score": 5,
        "total_possible": 10,
        "category": "history",
        "difficulty": "easy",
        "timed": False,
    }
    response = client.post("/api/submit-score", json=payload)
    assert response.status_code == 400


def test_submit_score_missing_field(client):
    """POST /api/submit-score missing a required field should return 400."""
    client.post("/api/set-name", json={"username": "TestUser"})
    response = client.post("/api/submit-score", json={"score": 5})
    assert response.status_code == 400


def test_leaderboard_route(client):
    """GET /api/leaderboard should return the top entries list."""
    response = client.get("/api/leaderboard")
    assert response.status_code == 200
    data = response.get_json()
    assert "entries" in data
    assert isinstance(data["entries"], list)


def test_history_route_no_user(client):
    """GET /api/history with no session user should return an empty list."""
    response = client.get("/api/history")
    assert response.status_code == 200
    assert response.get_json()["history"] == []


def test_history_route_with_user(client):
    """GET /api/history after setting a name should return a list."""
    client.post("/api/set-name", json={"username": "TestUser"})
    response = client.get("/api/history")
    assert response.status_code == 200
    assert isinstance(response.get_json()["history"], list)
