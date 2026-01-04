#backend/password_reset
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
import secrets
import os
import smtplib
from email.message import EmailMessage
from fastapi import Depends
from models import User
from database import get_db
from passlib.context import CryptContext

"""
Token generálás e-mailben
Jelszó frissítése token alapján
SMTP emailküldés
Token tárolása adatbázisban
Környezeti változók használata
"""
# ======================================================
# OOP + DEKLARATÍV
# - Pydantic modellek objektumként kezelhetők
# - SQLAlchemy ORM lekérdezések deklaratívan írják le az adatbázis logikát
# ======================================================
router = APIRouter()

class PasswordResetRequest(BaseModel):
    email: str
# ======================================================
# PROCEDURÁLIS PROGRAMOZÁS
# - Lépésről lépésre végrehajtott jelszó reset logika
# ======================================================
@router.post("/auth/password-reset/")  # app helyett router
def password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email nem található")

    token = secrets.token_urlsafe(32)
    user.password_reset_token = token
    db.commit()

    msg = EmailMessage()
    msg['Subject'] = "Jelszó visszaállítás"
    msg['From'] = "noreply@moziapp.com"
    msg['To'] = user.email

    frontend_url = os.getenv("FRONTEND_URL")  # .env-ből olvassa, nincs fallback localhost
    #msg.set_content(f"Kattints ide a jelszó visszaállításához: {frontend_url}/reset-password?token={token}")
    msg.set_content(f"Kattints ide a jelszó visszaállításához: {frontend_url}/reset_password?token={token}")

    # STARTTLS (587-es port)
    with smtplib.SMTP(os.getenv("SMTP_HOST", "smtp.gmail.com"), int(os.getenv("SMTP_PORT", 587))) as server:
        server.starttls()
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
        server.send_message(msg)

    return {"detail": "Jelszó visszaállító email elküldve."}

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ======================================================
# PROCEDURÁLIS + DEKLARATÍV + OOP
# - Hash-elés funkcionális, ORM műveletek deklaratívak
# ======================================================
@router.post("/auth/password-reset/confirm/")
def password_reset_confirm(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.password_reset_token == request.token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Érvénytelen vagy lejárt token")

    user.hashed_password = pwd_context.hash(request.new_password)
    user.password_reset_token = None
    db.commit()


    return {"detail": "A jelszó sikeresen módosítva."}


