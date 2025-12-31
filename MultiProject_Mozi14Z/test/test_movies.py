#test/test_movies.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)



def get_token():
    #user létrehozása
    client.post("/auth/register", json={
        "username": "test",
        "email": "test@example.com",
        "password": "password123"
    })
    #login
    r = client.post("/auth/token", data={
        "username": "test",
        "password": "password123"
    })
    assert r.status_code == 200
    return r.json()["access_token"]

@pytest.mark.parametrize("title,year", [("Inception", 2010), ("Avatar", 2009)])
def test_create_and_get_movie(title, year):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "title": title,
        "year": year,
        "genre": "Sci-Fi",
        "rating": 8.5,
        "description": "Test movie",
        "poster_url": None
    }
    r = client.post("/movies/", json=payload, headers=headers)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == title

    # film lekérése
    r2 = client.get(f"/movies/{data['id']}", headers=headers)
    assert r2.status_code == 200
    assert r2.json()["id"] == data["id"]