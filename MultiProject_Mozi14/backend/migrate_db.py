# backend/migrate_db.py
from database import Base, engine
from models import Movie  # feltételezve, hogy van Movie modell
from sqlalchemy.orm import Session
import sqlite3

# 1️⃣ Adatbázis táblák létrehozása
Base.metadata.create_all(bind=engine)

# 2️⃣ Lokális movies.db adatainak importálása
src_db_path = "movies.db"  # repo-beli SQLite db
dest_session = Session(bind=engine)

conn = sqlite3.connect(src_db_path)
cursor = conn.cursor()
cursor.execute("SELECT id, title, rating, description FROM movies")
rows = cursor.fetchall()

for row in rows:
    movie = Movie(id=row[0], title=row[1], rating=row[2], description=row[3])
    dest_session.merge(movie)  # merge biztosítja, hogy ne duplikáljon
dest_session.commit()
dest_session.close()
conn.close()

print("Migráció kész!")
