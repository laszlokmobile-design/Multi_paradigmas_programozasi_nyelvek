import streamlit as st
import requests

API_BASE = st.secrets["laszAPI_BASE"]

try:
    r = requests.get(f"{API_BASE}/")
    if r.status_code == 200:
        st.success("Backend elérhető! 🎉")
        st.json(r.json())
    else:
        st.error(f"Hiba a backendnél: {r.status_code}")
except Exception as e:
    st.error(f"Nem sikerült elérni a backendet: {e}")
