import streamlit as st
import folium
from streamlit.components.v1 import html
import json
import os

from data_fetch import get_gdelt_data
from processing import process_data

# ----------------------
# CONFIG
# ----------------------
st.set_page_config(page_title="OSINT Monitor", layout="wide")

CACHE_FILE = "data.json"

# ----------------------
# TITULO
# ----------------------
st.title("🌍 OSINT Global Intelligence System")
st.caption("Real-time monitoring of protests, conflicts and global risks")

# ----------------------
# BOTON REFRESH
# ----------------------
if st.button("🔄 Refresh Data"):
    articles = get_gdelt_data("protest")

    if articles:
        with open(CACHE_FILE, "w") as f:
            json.dump(articles, f)
        st.success("Data updated")
    else:
        st.warning("⚠️ API limit reached, try again later")

# ----------------------
# CARGA DE DATOS (CACHE)
# ----------------------
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        articles = json.load(f)
else:
    articles = get_gdelt_data("protest")

    if articles:
        with open(CACHE_FILE, "w") as f:
            json.dump(articles, f)

# ----------------------
# PROCESAMIENTO
# ----------------------
df = process_data(articles)

# ----------------------
# VALIDACIÓN
# ----------------------
if df.empty:
    st.error("⚠️ No data available (API limit). Please wait a few seconds and refresh.")
    st.stop()

# ----------------------
# METRICAS
# ----------------------
col1, col2, col3 = st.columns(3)

col1.metric("🌍 Total Events", len(df))
col2.metric("🚨 Alerts", int(df["alert"].sum()))
col3.metric("🌐 Countries", df["country"].nunique())

# ----------------------
# FILTRO
# ----------------------
countries = df["country"].unique()
selected = st.selectbox("🌐 Filter by country", ["All"] + list(countries))

if selected != "All":
    df = df[df["country"] == selected]

# ----------------------
# FILTRO ALERTAS
# ----------------------
only_alerts = st.checkbox("🚨 Show only critical events")

if only_alerts:
    df = df[df["alert"] == True]

# ----------------------
# MAPA
# ----------------------
st.subheader("🌍 Global Event Map")

m = folium.Map(location=[20, 0], zoom_start=2)

for _, row in df.iterrows():
    color = "red" if row["alert"] else "green"

    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=row["title"],
        icon=folium.Icon(color=color)
    ).add_to(m)

html(m._repr_html_(), height=500)

# ----------------------
# TABLA
# ----------------------
st.subheader("📊 Event Data")
st.dataframe(df)