#backend/models.py
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, func,Boolean
from .database import Base
from datetime import datetime

"""
A models.py az adatbázis szerkezetét definiálja.
A User a felhasználókat, a Movie a filmeket kezeli.
Ezeket a modelleket a CRUD műveletek, a scheduler és a REST API használja.
Nem fut „magától”, csak importáláskor és adatbázis-műveleteknél érvényesülnek.
"""

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=False)
    password_reset_token = Column(String, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    year = Column(Integer, nullable=True)
    genre = Column(String(100), nullable=True)
    rating = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    poster_url = Column(String(1000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    notified = Column(Boolean, default=False)  # <-- új mező