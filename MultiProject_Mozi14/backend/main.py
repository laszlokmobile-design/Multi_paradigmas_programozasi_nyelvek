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




@app.on_event("startup")
def on_startup():
    #4️⃣ Logger indítása
    logger.info("Starting Mozi API")

    # ✅ TÁBLÁK LÉTREHOZÁSA
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables checked/created")
    
    # Scheduler indítása (daemon thread)
    # Indítsd csak ha környezeti változó szerint engedélyezett (pl. BACKGROUND=true)
    if os.getenv("BACKGROUND_ENABLED", "true").lower() == "true":
        # 5️⃣ Scheduler indítása: task.py futtatása
        start_scheduler_in_thread()  # a fetch_new_movies scheduler
        start_email_scheduler()       # az email scheduler
        #threading.Thread(target=run_scheduler, daemon=True).start()


@app.get("/")
async def root():
    return {"message": "Mozi API fut!"}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}



