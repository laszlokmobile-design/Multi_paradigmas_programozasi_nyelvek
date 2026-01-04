#backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
#1️⃣ Környezeti változók betöltése
# ======================================================
# DEKLARATÍV PROGRAMOZÁS
# - Környezeti változók, konfigurációk
# ======================================================
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
# ======================================================
# OBJEKTUMORIENTÁLT PROGRAMOZÁS
# - Engine és Session objektumok
# ======================================================
#2️⃣ SQLAlchemy engine létrehozása
# SQLite esetén connect_args szükséges
#connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, echo=True)

#3️⃣ Session létrehozása
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
#4️⃣ Base osztály
Base = declarative_base()
# ======================================================
# FUNKCIONÁLIS PROGRAMOZÁS
# - FastAPI függvény, újrafelhasználható
# ======================================================
# 5️⃣ FastAPI függőség
# Függőség FastAPI-hez
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
