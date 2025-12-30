#backend/api/movies.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import crud 
import schemas
from database import SessionLocal
from auth import get_current_user
from email_utils import send_email, build_new_movie_email

router = APIRouter(prefix="/movies", tags=["movies"])

def get_db(): #Adatbázis kapcsolat
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.MovieRead])#Dekorátor, ilmek listázása
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):#Aláírás
    return crud.get_movies(db, skip=skip, limit=limit)

@router.get("/{movie_id}", response_model=schemas.MovieRead)#konkrét film lekérése
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    m = crud.get_movie(db, movie_id)
    if not m:
        raise HTTPException(status_code=404, detail="Movie not found")
    return m


"""
✔ Új filmet hoz létre az adatbázisban
✔ Csak autentikált felhasználó használhatja
✔ Automatikusan emailt küld minden regisztrált felhasználónak
✔ A háttérben végzi az emailküldést
✔ 201-es státuszkóddal visszaadja a létrehozott filmet
"""
@router.post("/", response_model=schemas.MovieRead, status_code=status.HTTP_201_CREATED)
def post_movie(
        movie: schemas.MovieCreate,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    new_movie = crud.create_movie(db, movie)
    # például

    # Minden regisztrált felhasználó email címét lekérjük
    user_emails = [u.email for u in crud.get_users(db) if u.email]

    # Értesítő email küldése
    background_tasks.add_task(
        send_email,
        "Új film a Mozi adatbázisban!",
        build_new_movie_email(new_movie.title, new_movie.year, new_movie.description),
        to_emails=user_emails
    )

    return new_movie

#statisztikai lekérdező végpont
@router.get("/stats/", tags=["movies"])
def stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)

