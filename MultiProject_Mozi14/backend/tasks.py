#backend/tasks.py
import os
import schedule, time, requests
from crud import create_movie
from database import SessionLocal
from schemas import MovieCreate
from datetime import datetime
import random
"""
✔ Minden nap 03:00-kor letölt 5 új termékadatot a dummy API-ból
✔ Ezeket „filmekként” hozzáadja az adatbázishoz
✔ Minden futás után kiír egy státuszüzenetet
"""

def fetch_new_movies():
    db = SessionLocal()
    try:
        response = requests.get("https://dummyjson.com/products?limit=5")
        data = response.json()["products"]
        for d in data:
            movie = MovieCreate(
                title=d["title"],
                year=2024,
                genre="Drama",
                rating=7.5,
                description=d["description"],
                poster_url=d["thumbnail"]
            )
            create_movie(db, movie)
        print("🎞️ Filmadatok frissítve!")
    finally:
        db.close()

def run_scheduler():
    schedule.every().day.at("03:00").do(fetch_new_movies)
    while True:
        schedule.run_pending()
        time.sleep(60)




TMDB_API_KEY = os.getenv("TMDB_API_KEY") 
BASE_URL = "https://api.themoviedb.org/3"

# Eddig lekért filmek ID-ja
seen_movie_ids = set()

def fetch_random_movie_db():
    db = SessionLocal()
    try:
        url = f"{BASE_URL}/movie/now_playing"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "hu-HU",
            "page": 1
        }
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()["results"]

        movie = random.choice(data)
        title = movie["title"]
        year = movie.get("release_date", "").split("-")[0]
        rating = movie.get("vote_average") or 7.5
        description = movie.get("overview") or ""
        poster_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else None

        # Mentés az adatbázisba
        db_movie = MovieCreate(
            title=title,
            year=int(year) if year else None,
            genre="Drama",
            rating=float(rating),
            description=description,
            poster_url=poster_url
        )
        create_movie(db, db_movie)
        print(f"🎬 {title} ({year}) ⭐ {rating}")
    except Exception as e:
        print(f"Hiba a film lekérésekor: {e}")
    finally:
        db.close()
