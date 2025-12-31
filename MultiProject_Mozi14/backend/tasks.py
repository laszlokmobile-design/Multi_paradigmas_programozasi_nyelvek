#backend/tasks.py
import os
import schedule, time, requests
from crud import create_movie, get_movie_by_title
from database import SessionLocal
from schemas import MovieCreate
import random

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
TMDB_API_KEY = os.getenv("TMDB_API_KEY") 
BASE_URL = "https://api.themoviedb.org/3"



def send_discord_message(content: str):
    if not DISCORD_WEBHOOK_URL:
        print("Webhook URL nincs beállítva")
        return
    data = {"content": content}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Hiba a Discord üzenetküldésnél: {e}")

def fetch_random_movie_db():
    db = SessionLocal()
    try:
        url = f"{BASE_URL}/movie/now_playing"
        params = {"api_key": TMDB_API_KEY, "language": "hu-HU", "page": 1}
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()["results"]

        movie = random.choice(data)
        title = movie["title"]

        # Ellenőrzés: már létezik-e
        if get_movie_by_title(db, title):
            print(f"A film már létezik: {title}")
            return

        year = movie.get("release_date", "").split("-")[0]
        rating = movie.get("vote_average") or 7.5
        description = movie.get("overview") or ""
        poster_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else None

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

        # Discord értesítés csak új film esetén
        send_discord_message(f"🎬 Új film az adatbázisban: **{title} ({year})** ⭐ {rating}")

    except Exception as e:
        print(f"Hiba a film lekérésekor: {e}")
    finally:
        db.close()
def run_scheduler():
    schedule.every().day.at("10:00").do(fetch_random_movie_db)

    while True:
        schedule.run_pending()
        time.sleep(60)


