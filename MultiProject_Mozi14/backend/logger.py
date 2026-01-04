#backend/logger.py
import logging

"""
A logger modulként működik, nem programként
Bármely más modul importálja, és az importáláskor a logging beállítás érvénybe lép
Önállóan nem fut
Fő “futtató” a main.py vagy bármely modul, ami használja a logger-t
"""
# ======================================================
# DEKLARATÍV PROGRAMOZÁS
# - Logging konfiguráció, formátum és szint beállítása
# ======================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s"
)
# ======================================================
# OBJEKTUMORIENTÁLT PROGRAMOZÁS
# - Logger objektum létrehozása és használata
# ======================================================
logger = logging.getLogger("mozi")
