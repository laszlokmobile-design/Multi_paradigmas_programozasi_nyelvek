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
"""
# ======================================================
# OBJEKTUMORIENTÁLT PROGRAMOZÁS
# - EmailMessage objektum használata
# ======================================================
def send_email(subject: str, body: str, to_emails: str| list[str] = None):
    if to_emails is None:
        to_emails = EMAIL_TO

    if isinstance(to_emails, str):
        to_emails = [to_emails]

    if not (SMTP_HOST and SMTP_USER and SMTP_PASSWORD and to_emails and EMAIL_FROM):
        logger.warning("SMTP not configured; skipping email.")
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg["To"] = ", ".join(to_emails)
    msg.set_content(body)

    context = ssl.create_default_context()
   # msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASSWORD)
            for email in to_emails:
                msg['To'] = email
                server.sendmail(EMAIL_FROM, email, msg.as_string())
        logger.info("Notification email sent.")

    except Exception as e:
        logger.error(f"Email sending failed: {e}")
"""
def send_email(subject: str, body: str, to_emails: str | list[str] = None):
    if to_emails is None:
        to_emails = EMAIL_TO

    if isinstance(to_emails, str):
        to_emails = [to_emails]

    if not (SMTP_HOST and SMTP_USER and SMTP_PASSWORD and to_emails and EMAIL_FROM):
        logger.warning("SMTP not configured; skipping email.")
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = ", ".join(to_emails)
    msg.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        logger.info("Notification email sent.")

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
