#backend/auth.py
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import SessionLocal
import crud
import schemas
from logger import logger
from dotenv import load_dotenv
from passlib.context import CryptContext
from urllib.parse import quote_plus

load_dotenv()
#1️⃣ JWT konfiguráció
SECRET_KEY = os.getenv("JWT_SECRET", "change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
# 2️⃣ OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
# 3️⃣ Access token létrehozása
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
# 4️⃣ Adatbázis-függőség
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# 5️⃣ Felhasználó autentikáció
def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_username(db, username)
    if not user:
        return None
    if not crud.verify_password(password, user.hashed_password):
        return None
    return user
# 6️⃣ Aktuális felhasználó lekérése tokenből
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 7️⃣ Jelszó hash-elés
def get_password_hash(password: str):
    # max 72 bájt
    password_bytes = password.encode("utf-8")[:72]

    return pwd_context.hash(password_bytes)
