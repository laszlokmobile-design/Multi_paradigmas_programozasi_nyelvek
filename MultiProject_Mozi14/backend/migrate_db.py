# backend/migrate_db.py
from database import Base, engine, SessionLocal
from models import Movie
import sqlite3
import os

# 1️⃣ Táblák létrehozása a cél DB-ben
Base.metadata.create_all(bind=engine)

# 2️⃣ Adatok átmásolása
src_db_path = os.path.join(os.path.dirname(__file__), "movies.db")  # biztos út
if not os.path.exists(src_db_path):
    print(f"Hiba: {src_db_path} nem található!")
    exit(1)

# új session
dest_session = SessionLocal()

# SQLite csatlakozás a repo db-hez
conn = sqlite3.connect(src_db_path)
cursor = conn.cursor()
cursor.execute("SELECT id, title, rating, description FROM movies")
rows = cursor.fetchall()

for row in rows:
    movie = Movie(id=row[0], title=row[1], rating=row[2], description=row[3])
    dest_session.merge(movie)

dest_session.commit()
dest_session.close()
conn.close()

print("Migráció kész!")

