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
@router.post("/auth/password-reset/")
def password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email nem található")

    token = secrets.token_urlsafe(32)
    user.password_reset_token = token
    db.commit()

    # --- JAVÍTÁS ITT KEZDŐDIK ---
    # 1. Beolvassuk a környezeti változót egy Python változóba
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8501") # Fallback, ha üres

    # 2. Összeállítjuk az üzenetet
    msg = EmailMessage()
    msg['Subject'] = "Jelszó visszaállítás"
    msg['From'] = smtp_user  # Most már létezik a változó!
    msg['To'] = user.email

    link = f"{frontend_url}/reset_password?token={token}"
    msg.set_content(f"Kattints ide a jelszó visszaállításához: {link}")

    # 3. Küldés hibakezeléssel (fontos Renderen!)
    try:
        # Fix adatok a hálózati hibák elkerülésére
        host = "smtp.gmail.com"
        port = 587 

        # Sima SMTP-t használunk (587), nem SMTP_SSL-t (465)
        with smtplib.SMTP(host, port, timeout=20) as server:
            server.starttls()  # Titkosítás aktiválása
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            print("✅ Email sikeresen elküldve!")
            
    except Exception as e:
        # Ha itt is hiba van, a Log-ban látni fogjuk a pontos okot
        print(f"❌ SMTP hiba: {e}")
        raise HTTPException(status_code=500, detail="Email küldési hiba.")

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






