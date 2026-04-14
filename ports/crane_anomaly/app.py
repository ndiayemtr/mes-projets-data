from pathlib import Path

import streamlit as st
import pandas as pd
import joblib

from utils import prepare_input

st.set_page_config(layout="wide")

st.title("Maintenance Prédictive des Portiques")

# Charger modèle + features

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "model.pkl")
features = joblib.load(BASE_DIR / "features.pkl")
df = pd.read_csv(BASE_DIR / "data.csv")

# =========================
# KPI GLOBAL
# =========================
st.subheader("État global des équipements")

col1, col2, col3 = st.columns(3)

col1.metric("Température moyenne", round(df["temperature"].mean(), 2))
col2.metric("Vibration moyenne", round(df["vibration"].mean(), 2))
col3.metric("Consommation moyenne", round(df["power_consumption"].mean(), 2))

st.divider()

# =========================
# HISTORIQUE
# =========================
st.subheader("Historique capteurs")

col1, col2 = st.columns(2)

with col1:
    st.line_chart(df["vibration"].head(1000))

with col2:
    st.line_chart(df["temperature"].head(1000))

st.divider()

# =========================
# INPUT UTILISATEUR
# =========================
st.sidebar.header("Paramètres du portique")

temp = st.sidebar.slider("Température", 30, 150, 70)
vib = st.sidebar.slider("Vibration", 1, 20, 5)
power = st.sidebar.slider("Consommation électrique", 50, 500, 200)
load = st.sidebar.slider("Charge", 0, 100, 30)
wind = st.sidebar.slider("Vent", 0, 50, 10)
hours = st.sidebar.slider("Heures fonctionnement", 1, 24, 6)

# =========================
# PRÉDICTION
# =========================
if st.button("Analyser état du portique"):

    input_data = prepare_input(temp, vib, power, load, wind, hours)

    # alignement features
    input_data = input_data.reindex(columns=features, fill_value=0)

    prediction = model.predict(input_data)[0]

    st.subheader("Résultat")

    col1, col2 = st.columns(2)

    if prediction == 1:
        col1.error("Risque de panne détecté")
    else:
        col1.success("Fonctionnement normal")

    col2.metric("Stress index", round(input_data["stress_index"].values[0], 2))

    st.divider()

    # =========================
    # INTERPRÉTATION
    # =========================
    st.subheader("Analyse")

    st.write(f"""
    - Température : {temp}
    - Vibration : {vib}
    - Consommation : {power}

    -> Le système détecte un état **{'critique' if prediction == 1 else 'normal'}**.
    """)

    # =========================
    # LOGIQUE MÉTIER
    # =========================
    if input_data["stress_index"].values[0] > 500:
        st.warning("Stress mécanique élevé — vérifier le portique")

    if vib > 10:
        st.warning("Vibration anormale détectée")

    if temp > 100:
        st.warning("Surchauffe possible")

    st.divider()

# =========================
# ANOMALIES HISTORIQUES
# =========================
st.subheader("Détection anomalies historiques")

threshold = df["vibration"].mean() + 2 * df["vibration"].std()

anomalies = df[df["vibration"] > threshold].copy()

# Création colonnes visuelles
anomalies["État Anomalie"] = anomalies["iso_pred"].map({
    -1: "🔴 Anomalie",
    1: "🟢 Normal"
})

anomalies["Prédiction Modèle"] = anomalies["rf_pred"].map({
    1: "🔴 Panne",
    0: "🟢 Normal"
})

# Affichage propre
st.dataframe(
    anomalies[[
        "temperature",
        "vibration",
        "power_consumption",
        "État Anomalie",
        "Prédiction Modèle"
    ]].head(50),
    use_container_width=True
)