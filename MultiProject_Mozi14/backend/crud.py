#backend/crud.py
from sqlalchemy.orm import Session
#from . import models, schemas
from typing import List, Optional
#from .auth import get_password_hash, pwd_context
#from .models import User  # igazítsd a helyes útvonalra
import models
import schemas
from auth import get_password_hash, pwd_context, MAX_BCRYPT_LENGTH
from models import User
from models import Movie

# ======================================================
# DEKLARATÍV PROGRAMOZÁS
# - Adatmodellek és típusok használata
# A SQLAlchemy ORM lekérdezések és típusannotációk
# deklaratív módon írják le az adatkezelést

# OBJEKTUMORIENTÁLT PROGRAMOZÁS
# - ORM modellek (User, Movie) objektumként kezelve

# FUNKCIONÁLIS PROGRAMOZÁS
# - Elkülönített, újrafelhasználható műveletek
# ======================================================

# 1️⃣ Users műveletek
# ------ Users ------
def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Truncate plain_password ugyanúgy, mint hash-eléskor
    password_bytes = plain_password.encode("utf-8")[:MAX_BCRYPT_LENGTH]
    return pwd_context.verify(password_bytes, hashed_password)
# ======================================================
# PROCEDURÁLIS PROGRAMOZÁS
# - Lépésről lépésre végrehajtott adatbázis műveletek
# ======================================================
#2️⃣ Movies műveletek
# ------ Movies ------
def get_movies(db: Session, skip: int = 0, limit: int = 100) -> List[models.Movie]:
    return db.query(models.Movie).order_by(models.Movie.created_at.desc()).offset(skip).limit(limit).all()

def get_movie(db: Session, movie_id: int) -> Optional[models.Movie]:
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def create_movie(db: Session, movie: schemas.MovieCreate) -> models.Movie:
    if movie.rating is None:
        movie.rating = 0.0
    obj = models.Movie(**movie.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    # Discord értesítés minden új filmnél
    try:
        from tasks import send_discord_message
        send_discord_message(
            f"🎬 Új film került az adatbázisba: **{obj.title} ({obj.year})** ⭐ {obj.rating}"
        )
    except Exception as e:
        print(f"Discord értesítés hiba: {e}")

    return obj


    
    # Új sor hozzáadásakor értesítés küldése
    try:
        from background import notify_new_movie
        notify_new_movie(obj)
    except Exception as e:
        # Hibakezelés, hogy a film létrehozása ne omoljon össze email hiba miatt
        print(f"Failed to send notification email: {e}")

    return obj

# ======================================================
# FUNKCIONÁLIS + DEKLARATÍV ELEMEK
# - Aggregáció és statisztika
# ======================================================
#Statisztika
def get_stats(db: Session):
    movies = db.query(models.Movie).all()
    count = len(movies)
    mean = None
    values = [m.rating for m in movies if m.rating is not None]
    if values:
        mean = sum(values) / len(values)
    return {"count": count, "mean_rating": mean}

# ======================================================
# FUNKCIONÁLIS PROGRAMOZÁS
# - Egyszerű lekérdezések
# ======================================================
# <-- Ezt a függvényt kell létrehozni:
def get_movie_by_title(db: Session, title: str):
    return db.query(Movie).filter(Movie.title == title).first()

def get_top10_movies(db: Session) -> List[str]:
    movies = db.query(Movie).all()
    # Rendezés rating alapján, majd lista comprehension a címekhez
    top10_titles = [m.title for m in sorted(movies, key=lambda m: m.rating or 0, reverse=True)[:10]]
    return top10_titles
