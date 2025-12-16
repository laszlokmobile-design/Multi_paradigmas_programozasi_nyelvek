# backend/seed.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, Movie   # <-- abszolút import

"""
✔ törli a régi adatbázist
✔ létrehoz egy újat
✔ hozzáad néhány előre megadott filmet
A kód akkor fut le ha kézzel elindítják
"""

# SQLite adatbázis elérési út
DB_PATH = "backend/movies.db"
DB_URL = f"sqlite:///{DB_PATH}"

# Motor létrehozása
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def populate_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️ Régi adatbázis törölve")

    Base.metadata.create_all(bind=engine)
    print("✅ Adatbázis és táblák létrehozva")

    db = SessionLocal()
    movies = [
        Movie(title="The Shawshank Redemption", year=1994, genre="Drama", rating=9.3,
              description="Two imprisoned men bond over a number of years...", poster_url="https://..."),
        Movie(title="The Godfather", year=1972, genre="Crime", rating=9.2,
              description="The aging patriarch of an organized crime dynasty transfers control...", poster_url="https://..."),
        Movie(title="Inception", year=2010, genre="Action, Sci-Fi", rating=8.8,
              description="A thief who steals corporate secrets through the use of dream-sharing technology...", poster_url="https://...")
    ]
    db.add_all(movies)
    db.commit()
    db.close()
    print("✅ Alapértelmezett filmek feltöltve az adatbázisba")


if __name__ == "__main__":
    populate_db()
