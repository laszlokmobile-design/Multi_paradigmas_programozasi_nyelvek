# ==== frontend/components/navigation.py ====
import streamlit as st


def sidebar_menu():
    return st.sidebar.radio(
    "Menü", ["Belépés", "Filmek", "Új film", "Statisztika", "Profil"]
    )