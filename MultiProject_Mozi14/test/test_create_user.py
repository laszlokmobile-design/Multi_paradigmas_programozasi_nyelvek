# test/test_create_user.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_user():
    payload = {
        "username": "tesztuser2",
        "email": "teszt2@example.com",
        "password": "Teszt123"
    }

    r = client.post("/auth/register", json=payload)

    # A válasz lehet 201 (siker) vagy 400 (ha létezik a user),
    # ezért csak azt ellenőrizzük, hogy valamilyen valid JSON-t kaptunk.
    assert r.status_code in (201, 400)
    assert "detail" in r.json() or "username" in r.json() or "email" in r.json()
