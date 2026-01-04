# backend/email_scheduler.py
import os
import smtplib
import ssl
from email.message import EmailMessage
import logging
from datetime import datetime, timedelta
import requests
import schedule
import time
import logging
from dotenv import load_dotenv
from database import SessionLocal
from models import User
"""
Ez a modul az előző napi filmfeltöltések értesítését automatizálja:
Lekéri a backendből az új filmeket
Összeállít egy emailt
Elküldi a címzetteknek
Naponta egyszer fut (ütemezett)
"""
# ======================================================
# DEKLARATÍV PROGRAMOZÁS
# - Konfigurációk és környezeti változók
# ======================================================
REMINDER_TIME = os.getenv("REMINDER_TIME", "09:00")  # alapértelmezett 09:00

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

logger = logging.getLogger("email_scheduler")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

API_BASE = os.getenv("API_BASE")  # .env-ből olvassa
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")  # pl. "teszt@example.com"
EMAIL_RECIPIENTS = [email.strip() for email in EMAIL_TO.split(",")]

API_TOKEN = os.getenv("API_TOKEN")

if not all([SMTP_USER, SMTP_PASSWORD, EMAIL_TO]):
    logging.error("Hiányzó SMTP vagy email konfiguráció! Ellenőrizd a környezeti változókat.")
    exit(1)

# ======================================================
# OBJEKTUMORIENTÁLT PROGRAMOZÁS
# - Session objektum és User modellek

# SessionLocal és User objektumok ORM-es használata
# (db.query(User).all() objektumorientált lekérdezés)

# FUNKCIONÁLIS PROGRAMOZÁS
# - Elkülönített, újrafelhasználható függvények
# ======================================================
def get_yesterdays_movies():
    """Lekéri az előző nap feltöltött filmeket a backendből"""
    yesterday = datetime.utcnow() - timedelta(days=1)
    headers = {"Authorization": f"Bearer {API_TOKEN}"} if API_TOKEN else {}
    try:
        r = requests.get(f"{API_BASE}/movies/", headers=headers, timeout=10)
        if r.status_code == 200:
            movies = r.json()
            y_movies = [m for m in movies if "created_at" in m and
                        datetime.fromisoformat(m["created_at"]) >= yesterday.replace(hour=0, minute=0, second=0, microsecond=0)]
            return y_movies
    except Exception as e:
        logging.error(f"Hiba a filmek lekérésekor: {e}")
    return []

def get_all_user_emails():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return [user.email for user in users]
    finally:
        db.close()

def send_email():
    logger.info("send_email() fut...")

    movies = get_yesterdays_movies()
    logger.info(f"Talált filmek száma: {len(movies)}")

    body = "Az előző nap feltöltött filmek:\n\n"

    if not movies:
        body += "Nincs új film az előző naphoz.\n"
    else:
        for m in movies:
            body += f"- {m['title']} ({m['year']}) – {m.get('genre', 'N/A')}\n"

    msg = EmailMessage()
    msg['Subject'] = "Előző napi filmfeltöltések"
    msg['From'] = SMTP_USER
    msg['To'] = ", ".join(get_all_user_emails())
    msg.set_content(body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            logger.info("SMTP login sikeres")
            server.send_message(msg)
            logger.info("Email elküldve!")
    except Exception as e:
        logger.error(f"Hiba az email küldésekor: {e}")


# Ütemezés: minden nap éjfélkor
#schedule.every().day.at("00:00").do(send_email)
#schedule.every(1).minutes.do(send_email)

# ======================================================
# PROCEDURÁLIS / IMPERATÍV PROGRAMOZÁS
# - Ütemezés és folyamatos futtatás
# ======================================================
def run_scheduler():
    import schedule
    import time
    logger.info("Email ütemező fut...")
    #schedule.every(10).seconds.do(send_email)  # debug: 10 mp, később napi egyszer
    schedule.every().day.at(REMINDER_TIME).do(send_email)
    while True:
        schedule.run_pending()
        time.sleep(1)




