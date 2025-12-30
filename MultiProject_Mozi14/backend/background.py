#backend/background.py
import threading
from time import sleep
import schedule
import requests
import smtplib
import ssl
import os
from email.message import EmailMessage
from database import SessionLocal
from schemas import MovieCreate
from logger import logger
from dotenv import load_dotenv
from notifications import notify_new_movies
#from backend.database import SessionLocal
from models import Movie, User
from email_utils import send_email, build_new_movie_email
from sqlalchemy.orm import Session
from email_utils import send_email as send_email_util
import time
import functools

load_dotenv()

SCRAPE_URL = os.getenv("SCRAPE_URL", "https://dummyjson.com/products?limit=3")
EMAIL_ON_NEW = os.getenv("EMAIL_ON_NEW", "false").lower() == "true"

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT") or 587)
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")  # can be comma separated
#1️⃣ SMTP email küldés funkció
def send_email(subject: str, body: str, to_emails: list[str] | None = None):
    if not (SMTP_HOST and SMTP_USER and SMTP_PASSWORD and EMAIL_FROM):
        logger.warning("SMTP not configured; skipping email.")
        return
    if not to_emails:
        logger.warning("No recipients provided; skipping email.")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(to_emails)
    msg.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        logger.info("Notification email sent.")
    except Exception as e:
        logger.exception("Failed to send email: %s", e)
# 2️⃣ Új filmek lekérése
def fetch_new_movies():
    from .crud import create_movie
    logger.info("Background: fetching new movies")
    try:
        r = requests.get(SCRAPE_URL, timeout=10)
        r.raise_for_status()
        data = r.json().get("products", [])
    except Exception as e:
        logger.exception("Failed to fetch remote data: %s", e)
        return

    db = SessionLocal()
    created = []
    try:
        for d in data:
            movie = MovieCreate(
                title=d.get("title", "untitled")[:300],
                year=2024,
                genre="Drama",
                rating=float(d.get("rating") or 7.0),
                description=d.get("description") or "",
                poster_url=d.get("thumbnail")
            )
            obj = create_movie(db, movie)
            created.append(obj)
        if created and EMAIL_ON_NEW:
            body = f"Created {len(created)} new movies:\n" + "\n".join([f"{m.id}: {m.title}" for m in created])
            send_email("Mozi: New movies added", body)
        logger.info("Background: saved %d items", len(created))
    finally:
        db.close()
# 3️⃣ Ütemezett futtatás
def scheduler_loop():
    # production: schedule.every().day.at("03:00").do(fetch_new_movies)
    # for dev/test: run every 5 minutes (uncomment during testing)
    # schedule.every(5).minutes.do(fetch_new_movies)
    schedule.every().day.at(os.getenv("SCRAPE_TIME", "03:00")).do(fetch_new_movies)
    while True:
        schedule.run_pending()
        sleep(10)

def start_scheduler_in_thread():
    t = threading.Thread(target=scheduler_loop, daemon=True)
    t.start()
    logger.info("Background scheduler started in thread")
"""
def scheduler_thread(): 
    schedule.every(1).minutes.do(notify_new_movies) 
    while True: 
        schedule.run_pending() 
        sleep(1)
"""
#4️⃣ Új film értesítés
def notify_new_movie(movie: Movie):
    db: Session = SessionLocal()
    users = db.query(User).all()
    emails = [user.email for user in users]
    if emails:
        subject = f"Új film: {movie.title}"
        body = build_new_movie_email(movie.title, movie.year, movie.description)
        send_email(subject, body, emails)
    db.close()
#5️⃣ Email scheduler
def start_email_scheduler():
    def email_loop():
        to_emails = [email.strip() for email in os.getenv("EMAIL_TO", "").split(",")]
        schedule.every().day.at("00:00").do(
            functools.partial(
                send_email_util,
                subject="Előző napi filmfeltöltések",
                body="Itt az összefoglaló a tegnapi filmekről...",
                to_emails=to_emails
            )
        )
        while True:
            schedule.run_pending()
            time.sleep(60)

    threading.Thread(target=email_loop, daemon=True).start()
