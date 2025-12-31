#backend/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from api import movies, auth as auth_router
from logger import logger
from background import start_scheduler_in_thread, start_email_scheduler
from database import engine, Base
from password_reset import router as password_reset_router
from tasks import run_scheduler
import threading
from tasks import fetch_random_movie_db
import time

#2️⃣ FastAPI app létrehozása
app = FastAPI(title="🎬 Mozi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # beadandóhoz OK
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#3️⃣ Routerek hozzáadása
app.include_router(auth_router.router)
app.include_router(movies.router)
app.include_router(password_reset_router)


def start_background_task():
    while True:
        try:
            fetch_random_movie_db()
        except Exception as e:
            print(f"[Background task hiba]: {e}")
        time.sleep(86400)  # naponta egyszer fut

@app.on_event("startup")
def on_startup():
    # Logger indítása
    logger.info("Starting Mozi API")

    # ✅ TÁBLÁK LÉTREHOZÁSA
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables checked/created")

    # Háttérfeladat: TMDb napi frissítés
    def start_background_task():
        while True:
            try:
                fetch_random_movie_db()
            except Exception as e:
                logger.error(f"[Background task hiba]: {e}")
            time.sleep(86400)  # naponta egyszer fut

    # TMDb háttérthread indítása
    threading.Thread(target=start_background_task, daemon=True).start()

    # Scheduler és e-mail (csak ha engedélyezve)
    if os.getenv("BACKGROUND_ENABLED", "true").lower() == "true":
        threading.Thread(target=start_scheduler_in_thread, daemon=True).start()
        threading.Thread(target=start_email_scheduler, daemon=True).start()
        logger.info("Background schedulers started")




@app.get("/")
async def root():
    return {"message": "Mozi API fut!"}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}



