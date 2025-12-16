#backend/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
"""
✔ adatok validálása
✔ API bejövő adatok kezelése (MovieCreate, UserCreate)
✔ API válaszmodellek (MovieRead, UserRead)
❗ A schemas.py NEM program, hanem modul.
❗ Csak importáláskor töltődik be.
❗ Nem kell külön futtatni.
❗ Automatikusan betöltődik, amikor FastAPI elindul.
"""
# User schemas
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Movie schemas
class MovieBase(BaseModel):
    title: str
    year: Optional[int] = None
    genre: Optional[str] = None
    rating: Optional[float] = 0.0
    description: Optional[str] = None
    poster_url: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class MovieRead(MovieBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True