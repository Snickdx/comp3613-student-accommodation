"""Shallow scenario smoke tests — intentionally weak."""

from fastapi.testclient import TestClient

from app.main import app
from app.seed import seed


def setup_module() -> None:
    seed(reset=True)


client = TestClient(app)


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["scenario"] == "student-accommodation"


def test_login_admin():
    r = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "admin-dev"},
    )
    assert r.status_code == 200
    assert r.json()["user"]["role"] == "admin"
    assert "password" not in r.json()["user"]


def test_student_browse():
    login = client.post(
        "/api/auth/login",
        json={"email": "student@example.com", "password": "stud-dev"},
    )
    uid = login.json()["user"]["id"]
    r = client.get("/api/student/listings", headers={"X-User-Id": str(uid)})
    assert r.status_code == 200
    assert isinstance(r.json()["listings"], list)
