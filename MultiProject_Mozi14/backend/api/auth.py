#backend/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
import schemas
from auth import create_access_token
from urllib.parse import quote_plus
from email_utils import send_email
from pydantic import BaseModel

class PasswordResetRequest(BaseModel):
    email: str

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():#Adatbázis kapcsolat
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/token") # Bejelentkezés
def login_for_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED) #Regisztráció
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user_in.username) or crud.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Username or email already registered")
    user = crud.create_user(db, user_in)
    return user

"""
@router.post("/password-reset/")
def password_reset(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Token létrehozása
    token = create_access_token({"sub": user.username})

    # Token URL-kódolása
    token_link = f"http://localhost:8501/reset_password?token={quote_plus(token)}"

    # Email küldése
    send_email(to=user.email, subject="Jelszó visszaállítás",
               body=f"Kattints ide a jelszó visszaállításhoz: {token_link}")

    return {"detail": "Password reset email sent"}
"""
@router.post("/password-reset/")
def password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    email = request.email
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Token létrehozása
    token = create_access_token({"sub": user.username})

    # Token URL-kódolása
    token_link = f"http://localhost:8501/reset_password?token={quote_plus(token)}"

    # Email küldése
    send_email(
        "Jelszó visszaállítás",
        f"Kattints ide a jelszó visszaállításhoz: {token_link}",
        user.email
    )


    return {"detail": "Password reset email sent"}
