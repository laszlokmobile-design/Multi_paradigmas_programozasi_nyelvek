  #backend/notifications.py
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Movie, User
from email_utils import send_email

def notify_new_movies():
    db: Session = SessionLocal()# Adatbázis kapcsolat létrehozása
    new_movies = db.query(Movie).filter(Movie.notified == False).all()# Lekéri az összes új filmet, amelyről még nem küldtek értesítést:
    if not new_movies:#Ha nincsenek új filmek, bezárja az adatbázist és kilép:
        db.close()
        return

    users = db.query(User).all()# Lekéri az összes felhasználó email címét
    emails = [user.email for user in users]

    # Minden új filmhez elküldi az értesítést a send_email függvénnyel:
    for movie in new_movies:
        send_email(
            subject=f"Új film a Mozi API-ban: {movie.title}",
            body=f"{movie.title} ({movie.year})\n\n{movie.description}",
            to_emails=emails
        )
        #Beállítja, hogy a filmről már értesítést küldtek:
        movie.notified = True
        #Mentés és kapcsolat lezárása
        db.add(movie)

    db.commit()

    db.close()
