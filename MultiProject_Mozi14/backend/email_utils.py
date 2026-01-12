#ackend/email_utils.py
import smtplib
import os
import ssl
import logging
from email.message import EmailMessage

"""
Ez a modul az email küldés logikáját tartalmazza
Segédfüggvényeket ad a többi modulnak (pl. notifications, password reset)
SMTP és SSL konfiguráció .env változókból
Hibakezelés és loggolás benne van
Nincs standalone futtatása
"""
# ======================================================
# FUNKCIONÁLIS PROGRAMOZÁS
# - Logger létrehozása, újrafelhasználható
# ======================================================
logger = logging.getLogger("email")

# ======================================================
# DEKLARATÍV PROGRAMOZÁS
# - Konfigurációk és környezeti változók
# ======================================================
# .env változók olvasása

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT") or 587)
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")  # can be comma separated

# ======================================================
# OBJEKTUMORIENTÁLT PROGRAMOZÁS
# - EmailMessage objektum használata
# ======================================================

def send_email(subject: str, body: str, to_emails: str | list[str] = None):
    # Használjuk a beállított célzott emailt vagy a környezeti változót
    if to_emails is None:
        to_emails = os.getenv("EMAIL_TO")

    if isinstance(to_emails, str):
        # Ha vesszővel elválasztott lista jön a .env-ből, szétbontjuk
        to_emails = [e.strip() for e in to_emails.split(",")]

    # FONTOS: A Gmailnél a FROM címnek meg kell egyeznie az USER címmel!
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    if not (smtp_user and smtp_password and to_emails):
        logger.warning("SMTP nincs konfigurálva; email küldés kihagyva.")
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    # A feladó MINDIG a saját hitelesített email címed legyen!
    msg['From'] = smtp_user 
    msg['To'] = ", ".join(to_emails)
    msg.set_content(body)

    context = ssl.create_default_context()

    try:
        # Renderen fixen az 587-es portot használjuk a hálózati hiba elkerülésére
        host = "smtp.gmail.com"
        port = 587

        with smtplib.SMTP(host, port, timeout=20) as server:
            server.starttls(context=context)  # Titkosítás indítása
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            logger.info("Email sikeresen elküldve (email_utils).")

    except Exception as e:
        logger.error(f"Email sending failed: {e}")
# ======================================================
# FUNKCIONÁLIS PROGRAMOZÁS
# - Tiszta függvény, bemenet → kimenet
# ======================================================
def build_new_movie_email(movie_title: str, movie_year: int, movie_description: str) -> str:
    return(
        f"Új film került a Mozi adatbázisába!\n\n"
        f"Cím: {movie_title}\n"
        f"Év: {movie_year}\n\n"
        f"Leírás: {movie_description}\n"
        f"Nézd meg az API-ban vagy a frontendben!"

    )

