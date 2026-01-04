# ==== frontend/components/charts.py ====
import streamlit as st
import pandas as pd
import altair as alt
"""
✔ Ellenőrzi az adat meglétét
✔ Megjeleníti az összes film számát
✔ Mutatja alap statisztikákat numerikus mezőkről
✔ Oszlopdiagramon szemlélteti a genre és rating kapcsolatát
"""
# ======================================================
# FUNKCIONÁLIS PROGRAMOZÁS
# - Elkülönített, újrafelhasználható függvény
# - Bemeneti adatokat kap, feldolgozza és megjeleníti
# ======================================================

def show_stats_chart(data: list):
    if not data:
        st.info("Nincs statisztikai adat.")
        return


    df = pd.DataFrame(data)
    st.metric("Összes film", len(df))
    st.write(df.describe())


    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(x=alt.X("genre:N"), y="rating:Q")
    )

    st.altair_chart(chart, use_container_width=True)
