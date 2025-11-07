import streamlit as st
import pandas as pd
import sqlite3
from streamlit_folium import st_folium
import folium
st.set_page_config(page_title="Suivi Livraisons", layout="wide")

st.title("🚚 Suivi en temps réel - Livraison IA")
conn = sqlite3.connect("data/deliveries.db")
# if table missing, show message
try:
    df = pd.read_sql("SELECT * FROM deliveries LIMIT 100", conn)
except Exception:
    df = pd.DataFrame(columns=["timestamp","client","lat","lon","meteo","temperature","traffic"])
st.subheader("Derniers points")
st.dataframe(df.head(20))

if not df.empty:
    last = df.iloc[-1]
    m = folium.Map(location=[last['lat'], last['lon']], zoom_start=12)
    for _,row in df.iterrows():
        folium.Marker([row['lat'], row['lon']], popup=f"{row['client']}").add_to(m)
    st_folium(m, width=800, height=500)
else:
    st.info("Aucune donnée de suivi trouvée. Lancez la simulation.")
