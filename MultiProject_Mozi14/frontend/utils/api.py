# ==== frontend/utils/api.py ====
import requests
import streamlit as st

"""
# ======================================================
# FUNKCIONÁLIS PROGRAMOZÁS
# - Elkülönített, újrafelhasználható függvények
# - Minden függvény egy konkrét feladatot lát el (login, regisztráció, lekérés, hozzáadás)
# ======================================================
✔ összekapcsolja a Streamlit frontendet a FastAPI back-enddel
✔ kezeli a login-t, regisztrációt, filmek lekérését, film hozzáadását
✔ automatikusan hozzáadja az Authorization Bearer JWT-t
✔ elrejti a backend URL-t és a networking részleteket
✔ egyszerű, használható függvényeket biztosít a frontend logikájának
"""
API_BASE = st.secrets["API_BASE"]#API címe

BASE_URL = "https://multiparadigmasprogramozasinyelvek-cjjaqkrmg6z9t9jkybdtam.onrender.com"

def _headers(): # token kezelés
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}

def login(username: str, password: str):
    return requests.post(
        f"{API_BASE}/auth/token",
        data={"username": username, "password": password},
    )

def register_user(data: dict):
    return requests.post(f"{API_BASE}/auth/register", json=data)

def get_movies():
    return requests.get(f"{API_BASE}/movies/", headers=_headers())

def add_movie(payload: dict):

    return requests.post(f"{API_BASE}/movies/", json=payload, headers=_headers())


