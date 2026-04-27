from pathlib import Path
import streamlit as st
import pandas as pd
from utils import predict_quality

st.set_page_config(layout="wide")

st.title("📡 Tableau de bord de surveillance de la qualité du réseau")

# ======================
# LOAD DATA
# ======================
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "data.csv")

# ======================
# KPI
# ======================
st.subheader("📊 Global KPI")

col1, col2, col3 = st.columns(3)

col1.metric("Mauvaise qualité  (%)", round((df["network_quality"]==0).mean()*100,2))
col2.metric("Période de pointe (%)", round(df["is_peak"].mean()*100,2))
col3.metric("Moyenne horaire", round(df["hour"].mean(),1))

st.divider()

# ======================
# FILTERS
# ======================
st.sidebar.header("🔎 Filtres")

network_filter = st.sidebar.multiselect(
    "Network Type Score",
    df["network_score"].unique(),
    df["network_score"].unique()
)

df_filtered = df[df["network_score"].isin(network_filter)]

# ======================
# CHARTS
# ======================
st.subheader("📊 Répartition de la qualité du réseau")
st.bar_chart(df_filtered["network_quality"].value_counts())

st.subheader("📊 Qualité vs heures de pointe")
st.bar_chart(df_filtered.groupby("is_peak")["network_quality"].mean())

st.subheader("📊 Utilisation horaire")
st.line_chart(df_filtered.groupby("hour").size())

st.divider()

# ======================
# SIMULATION
# ======================
st.sidebar.header("🎯 Simulation")

hour = st.sidebar.slider("Hour", 0, 23, 12)
is_peak = st.sidebar.selectbox("Peak", [0,1])
network = st.sidebar.selectbox("Network Score", [1,2,3])
location = st.sidebar.selectbox("Location Risk", [1,2,3])
weather = st.sidebar.selectbox("Weather Impact", [0,1,2])
speed = st.sidebar.slider("Speed Efficiency", 0.0, 1.0, 0.5)

if st.sidebar.button("Prédire la qualité"):
    
    input_data = {
        "hour": hour,
        "is_peak": is_peak,
        "network_score": network,
        "location_risk": location,
        "weather_impact": weather,
        "speed_efficiency": speed
    }

    pred, proba = predict_quality(input_data)

    st.subheader("🔮 Prediction")

    col1, col2 = st.columns(2)

    labels = {0: "🔴 Mauvais", 1: "🟠 Moyenne", 2: "🟢 Bon"}

    col1.metric("Prediction", labels[pred])

    col2.write("Probabilités:")
    st.write({
        "Mauvais ": round(proba[0]*100,2),
        "Moyenne": round(proba[1]*100,2),
        "Bon": round(proba[2]*100,2)
    })