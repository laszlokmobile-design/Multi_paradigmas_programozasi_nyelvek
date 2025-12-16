# ==== frontend/components/add_movie_form.py ====
import streamlit as st

def add_movie_form(on_submit):
    with st.form("add_movie_form"):
        title = st.text_input("Cím")
        year = st.number_input("Év", min_value=1900, max_value=2100, value=2024)
        genre = st.text_input("Műfaj")
        rating = st.slider("Értékelés", 0.0, 10.0, 5.0)
        description = st.text_area("Leírás")
        poster_url = st.text_input("Poster URL")

        submitted = st.form_submit_button("Hozzáadás")
        if submitted:
            payload = {
                "title": title,
                "year": int(year),
                "genre": genre,
                "rating": float(rating),
                "description": description,
                "poster_url": poster_url or None,
            }
            on_submit(payload)