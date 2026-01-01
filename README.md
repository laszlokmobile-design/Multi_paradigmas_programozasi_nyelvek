!!!!!!!!!!!!!!!!!!!

!!!FONTOS!!!

!!!!!!!!!!!!!!!!!!!

MultiProject_Mozi14 mappa: a projekt deployolásra került a Streamlit és a Render felületen, de a Gmail automata levélküldést a Render nem engedélyezi. Helyette discord üzenetet küld.

Streamlit DEPLOY: https://multiparadigmasprogramozasinyelvek-cjjaqkrmg6z9t9jkybdtam.streamlit.app/

Render DEPLOY:
https://mozi-backend-21wo.onrender.com/
https://dashboard.render.com/web/srv-d5115dur433s739muo6g

MultiProject_Mozi14Z mappa: Legfrissebb Localhostos verzió. Itt működik az automata levélküldés. Dockerizálás.

******************************************************************************************************************************************************************************************************************************************************************************
🎬 Movie Reminder – FastAPI + Streamlit Mikroszerviz Rendszer
Ez a projekt egy mikroszerviz-szerű Python alapú alkalmazás, amely egy filmadatbázist kezel, automatikus e-mail emlékeztetőket küld, vizualizációt jelenít meg, és külön backend + frontend komponensekből áll.

A beadandó célja:

modern Python eszközök használata,
többprogramozási paradigma (OOP + funkcionális + procedurális),
adatbáziskezelés ORM-mel,
aszinkron és ütemezett folyamatok,
webes felület (Streamlit),
REST API backend (FastAPI).
🚀 Funkciók
FastAPI REST backend
Filmek listázása, hozzáadása, törlése
Felhasználók kezelése
Token alapú autentikáció
Automatikus napi figyelmeztetések
Streamlit frontend
Filmek megjelenítése
Új film hozzáadása
Statisztikai vizualizáció (diagram)
Backend API hívások
Adatbázis – SQLAlchemy ORM
SQLite alapú adatmodell
Movies és Users táblák
Automatizált háttérfolyamat
Napi egyszeri ütemezett email küldés arról hogy az előző nap töltöttek e fel filmet az adatbázisba
schedule modul
SMTP alapú levelezés
Tesztelés – pytest
3 db teszt
1 parametrize-os teszt
HTTPX teszt kliens FastAPI-hoz
Deploy támogatás
FastAPI → Render
Streamlit → Streamlit Cloud
Környezeti változók .env fájlban
Hibakezelés:
A backend minden API végpontja try/except blokkokkal van védve, így az esetleges hibák nem omlasztják össze az
alkalmazást. Kezeljük az adatbázis műveletek, e-mail küldés és API hívások során fellépő hibákat. A hibák a logba
kerülnek, és szükség esetén a felhasználónak is jelezhetők.
Logolás:
A projekt a Python logging modulját használja.

INFO: normál működési üzenetek (pl. film hozzáadása, sikeres API hívás)

WARNING: nem kritikus problémák

ERROR: kritikus hibák (pl. adatbázis kapcsolat megszakadása)

A logok alapértelmezés szerint a konzolon jelennek meg, de a jövőben könnyen konfigurálható fájlba írásra is.

🧱 Projekt architektúra
# 🧱 Projekt architektúra
project/
│
├── backend/
│ ├── api/
│ ├──__init__.py (Python package)
│ │   ├── auth.py
│ │   └── movies.py
│ ├── .env
│ ├── __init__.py (Python package)
│ ├── auth.py
│ ├── background.py
│ ├── crud.py
│ ├── database.py
│ ├── Dockerfile
│ ├── email_scheduler.py
│ ├── email_utils.py
│ ├── logger.py
│ ├── main.py
│ ├──models.py
│ ├──notifications.py
│ ├──password_reset.py
│ ├──requirements.txt
│ ├──schemas.py
│ ├──seed.py
│ └──tasks.py
│
├── frontend/
│ ├── components
│ │   ├── __init__.py (Python package)
│ │   ├──add_movie_form.py
│ │   ├──auth_forms.py
│ │   ├──charts.py
│ │   ├──movie_list.py
│ │   └──navigation.py 
│ ├──  utils
│ │    ├── __init__.py (Python package)
│ │    └── api.py
│ ├──__init__.py (Python package)
│ ├──app.py
│ ├──Dockerfile
│ └──requirements.txt
│
├── tests/
│ ├── __init__.py (Python package)
│ ├── test_create_user.py
│ ├── test_email.py
│ └── test_movies.py
│
│
├── .env example
├── docker-compose.yml
├── main.py
├── movies.db
├── requirements.txt
├──README.md
├──start_backend.sh
├──start_frontend.sh
└──test.db

🔹 Hibakezelés és logolás (példa) backend/logger.py import logging

logger = logging.getLogger("movie_reminder") logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler() formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') console_handler.setFormatter(formatter) logger.addHandler(console_handler)

backend/api/movies.py from fastapi import APIRouter, HTTPException from backend.logger import logger

router = APIRouter()

@router.get("/movies") async def get_movies(): try: movies = ["Film1", "Film2"] logger.info("Sikeresen lekértük a filmeket.") return {"movies": movies} except Exception as e: logger.error(f"Hiba a filmek lekérésekor: {e}") raise HTTPException(status_code=500, detail="Hiba történt a filmek lekérésekor.")

backend/email_scheduler.py from backend.logger import logger

def send_email(to_email: str, subject: str, body: str): try: logger.info(f"Email küldése {to_email} címre...") # SMTP kód itt logger.info("Email sikeresen elküldve.") except Exception as e: logger.error(f"Hiba az email küldésekor: {e}")

🧱 Projekt architektúra és nyelvek Fájl / Könyvtár Nyelv / Formátum Megjegyzés backend/main.py Python FastAPI entry point backend/logger.py Python Logolás backend/api/movies.py Python REST API endpoint backend/api/auth.py Python Auth API, JWT kezelése backend/database.py Python SQLAlchemy setup backend/email_scheduler.py Python Email küldés frontend/app.py Python Streamlit frontend frontend/components/movie_list.py Python Streamlit komponens frontend/utils/api.py Python Backend hívások segédje tests/test_movies.py Python Unit / API teszt .env INI / Environment Környezeti változók
Programozási paradigmák: 1️⃣ OOP (Objektum-orientált programozás)

Jellemző: osztályok, példányok, metódusok, enkapszuláció.

Példák a projektben:

Fájl Miben OOP backend/models.py SQLAlchemy ORM osztályok (Movie, User) – adattáblák modellezése osztályokkal backend/database.py Ha van DatabaseSession vagy wrapper osztály az adatbázis kezelésére backend/email_utils.py Ha EmailSender osztály van (SMTP logika kapszulázása) frontend/components/*.py Streamlit komponensek, pl. MovieList, ha osztályban definiálják az UI logikát backend/logger.py Logger osztály, ha van wrapper a Python logging modul fölött 2️⃣ Funkcionális programozás

Jellemző: függvények, stateless logika, list comprehension, map/filter/reduce.

Példák a projektben:

Fájl Funkcionális elem backend/crud.py Adatbázis műveletek függvényekkel (get_movie, add_movie) backend/api/*.py Endpoint függvények (@router.get, @router.post) – stateless REST logika frontend/utils/api.py Backend hívásokat végző függvények (get_movies(), add_movie()) frontend/components/charts.py Adatok feldolgozása list comprehensionnel, Pandas/Altair plot függvények 3️⃣ Procedurális programozás

Jellemző: lineáris utasítások, script-szerű futtatás.

Példák a projektben:

Fájl Procedurális elem backend/main.py uvicorn.run() hívás, API inicializálás, route regisztráció frontend/app.py Streamlit app futtatása, lineáris UI logika (st.title(), st.button()) backend/email_scheduler.py Schedule logika: lineáris script, ami időzített feladatot futtat tests/*.py Tesztek futtatása, setup/teardown logika procedurális módon Összegzés

OOP: modellek, komponensek, wrapper osztályok

Funkcionális: REST endpointok, adatfeldolgozó függvények

Procedurális: fő script futtatása, schedule logika, teszt setup

⚙️ Telepítés és futtatás
1️⃣ Virtuális környezet létrehozása
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

2️⃣ Könyvtárak telepítése
pip install -r requirements.txt

3️⃣ Backend indítása (FastAPI)
uvicorn main:app --reload


Backend elérés:
http://127.0.0.1:8000

Swagger dokumentáció:
http://127.0.0.1:8000/docs

4️⃣ Frontend indítása (Streamlit)
streamlit run frontend/app.py

🔐 .env sablon
DATABASE_URL=sqlite:///./movies.db

JWT_SECRET_KEY=your_secret_key
ALGORITHM=HS256

EMAIL_SENDER=youremail@gmail.com
EMAIL_PASSWORD=your_app_password

REMINDER_TIME=09:00

🚀 Deploy útmutató
🔵 Backend deploy (Render.com): https://mozi-backend-21wo.onrender.com/
https://dashboard.render.com/web/srv-d5115dur433s739muo6g

Új Web Service létrehozása

GitHub repository: https://github.com/laszlokmobile-design/Multi_paradigmas_programozasi_nyelvek/

Start command:

uvicorn main:app --host 0.0.0.0 --port 10000


Environment → .env változók hozzáadása

Build & Deploy

🟣 Frontend deploy (Streamlit Cloud)

Új app létrehozása

Repository + file: frontend/app.py

Environment → Secret variables → ugyanazok a .env értékeid

Deploy LINK: https://multiparadigmasprogramozasinyelvek-cjjaqkrmg6z9t9jkybdtam.streamlit.app/

📊 Vizualizáció (Altair + Pandas)

A Streamlit frontend tartalmaz:

filmek száma

kategória szerinti eloszlás

diagram megjelenítés Altairrel

🧪 Tesztek futtatása
pytest -v


A tesztek tartalmaznak:

API endpoint tesztet HTTPX-szel

Unit tesztet

@pytest.mark.parametrize tesztet

📚 Felhasznált technológiák
Terület	Technológia
Backend	FastAPI, Uvicorn
Frontend	Streamlit
ORM	SQLAlchemy
Validáció	Pydantic
Ütemezés	schedule
Email	smtplib, email.mime
Vizualizáció	Altair, Pandas
Tesztelés	pytest, httpx
📌 Fejlesztői információk

Python 3.10+

Teljes PEP8 kompatibilis kód

Moduláris, mikroszerviz jellegű struktúra

Könnyen bővíthető új API-kal vagy új vizualizációval


### DOCKER HIBA: (CSAK LOCALHOST) ###
A Docker Compose nem tud új konténert létrehozni ugyanazzal a névvel, amíg a régi konténer létezik.
Megoldás lépésről lépésre:

1. Listázd a konténereket (futó és leállított):

docker ps -a


Ez kilistázza az összes konténert, és láthatod a fastapi-backend konténert.

2. Távolítsd el a konfliktusos konténert:

docker rm -f fastapi-backend


A -f kapcsoló biztosítja, hogy ha fut a konténer, leállítja és törli is.

3. Ellenőrizd, hogy nincs már névütközés:

docker ps -a


Győződj meg róla, hogy nincs fastapi-backend név.

4. Indítsd újra a Docker Compose-t:

docker-compose up --build
