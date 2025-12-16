#backend/tasks.py
import schedule, time, requests
from .crud import create_movie
from .database import SessionLocal
from .schemas import MovieCreate

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
