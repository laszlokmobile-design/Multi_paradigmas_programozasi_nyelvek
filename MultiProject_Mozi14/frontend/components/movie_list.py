# ==== frontend/components/movie_list.py ====
import streamlit as st
import pandas as pd
import altair as alt

# ======================================================
# FUNKCIONÁLIS PROGRAMOZÁS
# - Elkülönített, újrafelhasználható függvény
# - Bemeneti adatokat kap (movies), feldolgozza és megjeleníti
# ======================================================
def show_movie_list(movies: list):
    if not movies:
        st.info("Nincs megjeleníthető film.")
        return


    df = pd.DataFrame(movies)
    st.dataframe(df[["id", "title", "year", "genre", "rating"]])

    # ======================================================
    # DEKLARATÍV PROGRAMOZÁS
    # - Altair grafikon deklaratívan írja le a vizualizációt
    # ======================================================
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(x=alt.X("title:N", sort="-y"), y="rating:Q")
        .properties(height=300)
    )

    st.altair_chart(chart, use_container_width=True)
