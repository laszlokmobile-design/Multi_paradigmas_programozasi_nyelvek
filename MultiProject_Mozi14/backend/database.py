#backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
#1️⃣ Környezeti változók betöltése
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./movies.db")

#2️⃣ SQLAlchemy engine létrehozása
# SQLite esetén connect_args szükséges
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

#3️⃣ Session létrehozása
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
#4️⃣ Base osztály
Base = declarative_base()

# 5️⃣ FastAPI függőség
# Függőség FastAPI-hez
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
