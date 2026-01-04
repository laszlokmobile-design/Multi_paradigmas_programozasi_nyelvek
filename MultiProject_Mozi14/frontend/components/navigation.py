# ==== frontend/components/navigation.py ====
import streamlit as st

# ======================================================
# FUNKCIONÁLIS PROGRAMOZÁS
# - Elkülönített, újrafelhasználható függvény
# - Bemeneti adat (nincs explicit paraméter) alapján visszaadja a választott menüpontot
# ======================================================

def sidebar_menu():
    return st.sidebar.radio(
    "Menü", ["Belépés", "Filmek", "Új film", "Statisztika", "Profil"]

    )
