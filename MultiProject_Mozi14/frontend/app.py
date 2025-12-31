#frontend/app.py
import os
import streamlit as st
import requests
import pandas as pd
import altair as alt
import urllib.parse

menu = None

# Felhasználótól bekérjük az emailt
#email = st.text_input("Email címed")
st.set_page_config(page_title="Mozi – Filmajánló", layout="wide")

# API base URL: előnyösen st.secrets-ben tárold (Streamlit Cloud esetén secrets)
# API base URL, secrets.toml-ból vagy default localhost
# Példa: a környezeti változó DOCKER_FRONTEND legyen "true" Docker esetén
if os.getenv("DOCKER_FRONTEND", "false").lower() == "true":
    API_BASE = "https://mozi-backend-21wo.onrender.com"
else:
    # Lokális futtatás
    API_BASE = st.secrets["API_BASE"]

# egyszerű token tárolás a session_state-ben
if "token" not in st.session_state:
    st.session_state.token = None

def api_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

# Backend elérhetőség ellenőrzése
def check_backend():
    try:
        r = requests.get(f"{API_BASE}/movies/", headers=api_headers(), timeout=5)
        r.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Nem lehet elérni a backend szolgáltatást: {e}")
        return False


st.markdown("<h1 style='font-size:50px;'>🎬 Mozi – Filmajánló rendszer</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:24px;'>Üdv a filmajánló alkalmazásban!</p>", unsafe_allow_html=True)

query_params = st.query_params
token_from_query = query_params.get("token")

#query_params = st.experimental_get_query_params()
#token_from_query = query_params.get("token", [None])[0]
if token_from_query:
    # Dekódolja a tokenben esetleg előforduló %-kódolt karaktereket
    token_from_query = urllib.parse.unquote(token_from_query)
    st.session_state.reset_token = token_from_query
    # Ha token jön a linkből, menü legyen automatikusan Jelszó visszaállítás
    st.session_state.menu = "Jelszó visszaállítás"
    #st.experimental_rerun()# <- törölni kell



# Sidebar menü mindig
if "menu" not in st.session_state:
    st.session_state.menu = "Belépés"
menu_options = ["Belépés", "Jelszó visszaállítás", "Filmek", "Új film", "Statisztika", "Profil"]
menu = st.sidebar.radio(
    "Menü",
    menu_options,
    index=menu_options.index(st.session_state.menu)
)
st.session_state.menu = menu

####################
# BELÉPÉS / REGISZTRÁCIÓ
####################


if menu == "Belépés":
    st.write("## Bejelentkezés")
    col1, col2 = st.columns(2)
    with col1:
        login_user = st.text_input("Felhasználónév", key="login_user")
    with col2:
        login_pass = st.text_input("Jelszó", key="login_pass", type="password")
    if st.button("Bejelentkezés"):
        # OAuth2 token endpoint expects form data (username, password)
        data = {"username": login_user, "password": login_pass}
        try:

           #r = requests.post(f"{API_BASE}/auth/token", data=data, timeout=10)
           r = requests.post(
               f"{API_BASE}/auth/token",  # OAuth2 login endpoint
               data={"username": login_user, "password": login_pass},
               timeout=10
           )

        except Exception as e:
            st.error(f"Nem sikerült elérni a szervert: {e}")
        else:
            if r.status_code == 200:
                st.session_state.reset_token = None  # <--- token törlése
                st.session_state.token = r.json().get("access_token")
                st.success("Sikeres bejelentkezés.")
            else:
                st.error("Bejelentkezés sikertelen. Ellenőrizd a felhasználót/jelszót.")

    st.write("## Elfelejtett jelszó")
    email_login = st.text_input("Email címed", key="email_login")  # egyedi key
    if st.button("Küldés"):
        r = requests.post(f"{API_BASE}/auth/password-reset/", json={"email": email_login})
        if r.status_code == 200:
            st.success("Email elküldve, ellenőrizd a postafiókod.")
        else:
            st.error(f"Hiba: {r.json()['detail']}")

    st.markdown("---")
    st.write("## Regisztráció")
    with st.form(key="reg_form"):
        reg_user = st.text_input("Felhasználónév (reg)", key="reg_user")
        reg_email = st.text_input("Email (reg)", key="reg_email")
        reg_pass = st.text_input("Jelszó (reg)", type="password", key="reg_pass")
        submitted = st.form_submit_button("Regisztráció")

    if submitted:
        if not reg_user.strip() or not reg_email.strip() or not reg_pass.strip():
            st.error("Minden mezőt kötelező kitölteni!")
        else:
            payload = {"username": reg_user.strip(), "email": reg_email.strip(), "password": reg_pass.strip()}
            try:
                r = requests.post(f"{API_BASE}/auth/register", json=payload, timeout=10)
            except Exception as e:
                st.error(f"Nem sikerült elérni a szervert: {e}")
            else:
                if r.status_code == 201:
                    st.success("Sikeres regisztráció — jelentkezz be.")
                else:
                    st.error(f"Hiba: {r.status_code} — {r.text}")

####################
# JELSZÓ VISSZAÁLLÍTÁS
####################
elif menu == "Jelszó visszaállítás":
    st.write("## Jelszó visszaállítása")

    token_input = st.session_state.get("reset_token", "")
    if not token_input:
        st.error("Érvénytelen link vagy hiányzó token.")
        st.stop()

    st.info("Token automatikusan betöltve a linkből.")

    st.text_input("Token", value=token_input, disabled=True)

    new_password = st.text_input("Új jelszó", type="password", key="new_password")
    confirm_password = st.text_input("Új jelszó újra", type="password", key="confirm_password")

    if st.button("Jelszó módosítása"):
        if new_password != confirm_password:
            st.error("A két jelszó nem egyezik!")
        elif len(new_password) < 6:
            st.error("A jelszónak legalább 6 karakter hosszúnak kell lennie.")
        else:
            try:
                r = requests.post(
                    f"{API_BASE}/auth/password-reset/confirm/",
                    json={"token": token_input, "new_password": new_password}
                )
            except Exception as e:
                st.error(f"Hálózati hiba: {e}")
            else:
                if r.status_code == 200:
                    st.success("A jelszó sikeresen módosítva! Jelentkezz be.")
                    st.session_state.menu = "Belépés"
                    st.experimental_rerun()
                else:
                    try:
                        st.error(f"Hiba: {r.json().get('detail')}")
                    except:
                        st.error("Ismeretlen hiba történt.")


####################
# FILMEK LISTÁJA + VIZUALIZÁCIÓ
####################
elif menu == "Filmek":
    st.write("## Filmek")
    # Nagyobb cím és leírás
    st.subheader("Filmek listája")
    st.markdown("<span style='font-size:20px;'>Ez a leírás nagyobb betűkkel jelenik meg.</span>",
                unsafe_allow_html=True)

    try:
        r = requests.get(f"{API_BASE}/movies/", headers=api_headers(), timeout=10)
        r.raise_for_status()
        items = r.json()
    except Exception as e:
        st.error(f"Hálózati hiba: {e}")
        items = []
    else:
        if r.status_code == 200:
            items = r.json()
            if items:
                df = pd.DataFrame(items)
                # rendezés
                if "created_at" in df.columns:
                    df["created_at"] = pd.to_datetime(df["created_at"])
                    df = df.sort_values("created_at", ascending=False)
             #   st.dataframe(df[["id", "title", "year", "genre", "rating"]].reset_index(drop=True))

                # Stílusos táblázat AgGrid-del
                from st_aggrid import AgGrid

                AgGrid(df[["id", "title", "year", "genre", "rating"]],
                       fit_columns_on_grid_load=True,
                       height=300,
                       theme='light',
                       enable_enterprise_modules=False)

                # Vizualizációk
                st.write("### Értékelés (rating) diagram")
                # ha vannak duplikált címek, lehet rövidíteni
                df_plot = df.copy()
                df_plot["title_short"] = df_plot["title"].str.slice(0, 30)
                chart = alt.Chart(df_plot).mark_bar().encode(
                    x=alt.X('title_short:N', sort='-y', title="Cím"),
                    y=alt.Y('rating:Q', title="Értékelés")
                ).properties(height=350)
                st.altair_chart(chart, use_container_width=True)

                # Szűrés: műfaj
                genres = sorted(df["genre"].dropna().unique().tolist())
                sel_genre = st.multiselect("Szűrés műfaj szerint", options=genres, default=None)
                if sel_genre:
                    df_f = df[df["genre"].isin(sel_genre)]
                    AgGrid(df_f[["id", "title", "genre", "rating"]],
                           fit_columns_on_grid_load=True,
                           height=300,
                           theme='light',
                           enable_enterprise_modules=False)
                  #  st.dataframe(df_f[["id","title","genre","rating"]])
            else:
                st.info("Nincs film az adatbázisban.")
        elif r.status_code == 401:
            st.warning("Nincs jogosultság – jelentkezz be.")
        else:
            st.error(f"Hiba: {r.status_code} — {r.text}")

####################
# ÚJ FILM HOZZÁADÁSA
####################
elif menu == "Új film":
    st.write("## Új film hozzáadása")
    if not st.session_state.token:
        st.warning("A film hozzáadásához be kell jelentkezned.")
    with st.form(key="add_movie"):
        title = st.text_input("Cím")
        year = st.number_input("Év", min_value=1800, max_value=2100, value=2024)
        genre = st.text_input("Műfaj")
        rating = st.slider("Értékelés", 0.0, 10.0, 5.0)
        description = st.text_area("Leírás")
        poster_url = st.text_input("Poster URL (opcionális)")
        submitted = st.form_submit_button("Hozzáadás")
        if submitted:
            payload = {
                "title": title,
                "year": int(year) if year else None,
                "genre": genre or None,
                "rating": float(rating),
                "description": description or None,
                "poster_url": poster_url or None
            }
            try:
                r = requests.post(f"{API_BASE}/movies/", json=payload, headers=api_headers(), timeout=10)
            except Exception as e:
                st.error(f"Hálózati hiba: {e}")
            else:
                if r.status_code in (200, 201):
                    st.success("Film sikeresen elmentve.")
                elif r.status_code == 401:
                    st.error("Nincs jogosultság: jelentkezz be.")
                else:
                    st.error(f"Hiba történt: {r.status_code} — {r.text}")

####################
# STATISZTIKA
####################
elif menu == "Statisztika":
    st.write("## Statisztika")
    try:
        r = requests.get(f"{API_BASE}/movies/stats/", headers=api_headers(), timeout=10)
        r.raise_for_status()
        stats = r.json()
    except Exception as e:
        st.error(f"Hálózati hiba: {e}")
        stats = {}
    else:
        st.metric("Összes film", stats.get("count", 0))
        mean = stats.get("mean_rating")
        st.metric("Átlag rating", f"{mean:.2f}" if mean else "N/A")
        st.json(stats)

 # Top10 filmek megjelenítése itt
    st.subheader("🎬 Top 10 film")
    try:
        r = requests.get(f"{API_BASE}/movies/top10", headers=api_headers(), timeout=10)
        r.raise_for_status()
        top10 = r.json().get("top10", [])
        if top10:
            for i, title in enumerate(top10, start=1):
                st.write(f"{i}. {title}")
        else:
            st.info("Nincs elérhető adat.")
    except Exception as e:
        st.error(f"Hiba a Top10 filmek lekérésekor: {e}")

####################
# PROFIL / KIJELENTKEZÉS
####################
elif menu == "Profil":
    st.write("## Profil")
    if st.session_state.token:
        st.write("Bejelentkezve.")
        if st.button("Kijelentkezés"):
            st.session_state.token = None
            st.success("Kijelentkeztél.")
    else:
        st.info("Nincs bejelentkezve.")

