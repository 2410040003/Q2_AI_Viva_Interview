
from fastapi.testclient import TestClient
from app.main import app
import app.main as main_module

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "AI Viva Interview System is running"


def test_start_interview(monkeypatch):
    def mock_start(name, subject, difficulty):
        return {
            "session_id": "test-session-123",
            "question_number": 1,
            "question": "What is Python?"
        }

    monkeypatch.setattr(
        main_module,
        "start_interview",
        mock_start
    )

    response = client.post(
        "/start-interview",
        json={
            "student_name": "Sai Kiran",
            "subject": "Python",
            "difficulty": "easy"
        }
    )

    assert response.status_code == 200
    assert response.json()["session_id"] == "test-session-123"
    assert response.json()["question_number"] == 1


def test_invalid_interview_input():
    response = client.post(
        "/start-interview",
        json={
            "student_name": "A",
            "subject": "Python",
            "difficulty": "easy"
        }
    )

    assert response.status_code == 422


def test_invalid_session():
    response = client.post(
        "/submit-answer",
        json={
            "session_id": "invalid-session",
            "answer": "Python is a programming language"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid session ID"
