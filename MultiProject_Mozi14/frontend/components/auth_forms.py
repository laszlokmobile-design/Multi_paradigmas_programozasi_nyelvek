# ==== frontend/components/auth_forms.py ====
import streamlit as st

def login_form(on_login):
    st.subheader("Bejelentkezés")
    username = st.text_input("Felhasználónév")
    password = st.text_input("Jelszó", type="password")
    if st.button("Belépés"):
        on_login(username, password)

def register_form(on_register):
    st.subheader("Regisztráció")
    username = st.text_input("Új felhasználónév")
    password = st.text_input("Jelszó", type="password")
    full_name = st.text_input("Teljes név")
    email = st.text_input("Email")

    if st.button("Regisztráció"):
        on_register(
            {
                "username": username,
                "password": password,
                "full_name": full_name,
                "email": email,
            }
        )