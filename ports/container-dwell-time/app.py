from pathlib import Path

import streamlit as st
import pandas as pd
import joblib

st.set_page_config(layout="wide")

st.title("Prédiction du temps de séjour des conteneurs")

# Charger modèle + features

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "model.pkl")
features = joblib.load(BASE_DIR / "features.pkl")
df = pd.read_csv(BASE_DIR / "data.csv")

# ================================
# INPUT UTILISATEUR (SIMPLIFIÉ)
# ================================

st.sidebar.header("Paramètres")

container_size = st.sidebar.selectbox("Taille conteneur", [20, 40])
customs_delay = st.sidebar.slider("Retard douane", 0, 10, 2)
is_peak_season = st.sidebar.selectbox("Saison haute", [0, 1])
month = st.sidebar.slider("Mois", 1, 12, 6)
day_of_week = st.sidebar.slider("Jour semaine (0=Lundi)", 0, 6, 2)
forwarder_volume = st.sidebar.slider("Volume transitaire", 0, 100, 50)

cargo_type = st.sidebar.selectbox(
    "Type marchandise",
    ["Electronics", "Rice", "Textile", "Vehicles"]
)

origin_country = st.sidebar.selectbox(
    "Pays origine",
    ["France", "India", "Morocco", "Turkey"]
)

forwarder = st.sidebar.selectbox(
    "Transitaire",
    ["DakarLog", "FastForward", "GlobalTrade", "SahelTransit"]
)

# ================================
# CONSTRUCTION INPUT
# ================================

# Créer un dataframe vide avec toutes les features
input_data = pd.DataFrame(columns=features)
input_data.loc[0] = 0  # initialiser à 0

# Remplir variables numériques
input_data["container_size"] = container_size
input_data["customs_delay"] = customs_delay
input_data["is_peak_season"] = is_peak_season
input_data["month"] = month
input_data["day_of_week"] = day_of_week
input_data["forwarder_volume"] = forwarder_volume

# Variables dérivées (IMPORTANT)
input_data["quarter"] = (month - 1) // 3 + 1
input_data["is_week"] = 1
input_data["week_of_year"] = 25  # simplification

# One-hot encoding manuel
input_data[f"cargo_type_{cargo_type}"] = 1
input_data[f"origin_country_{origin_country}"] = 1
input_data[f"freight_forwarder_{forwarder}"] = 1

# ================================
# PRÉDICTION
# ================================

if st.button("Prédire"):
    
    # Aligner colonnes (sécurité)
    input_data = input_data.reindex(columns=features, fill_value=0)
    
    prediction = model.predict(input_data)[0]
    
    # ================================
    # AFFICHAGE DASHBOARD
    # ================================
    
    col1, col2 = st.columns(2)
    
    col1.metric("Temps de séjour estimé (jours)", round(prediction, 2))
    
    if prediction < 3:
        col2.success("Flux fluide")
    elif prediction < 7:
        col2.warning("Congestion modérée")
    else:
        col2.error("Forte congestion")

    st.subheader("Historique du temps de séjour des conteneurs")
    df_clean = df.copy()
    df_clean["dwell_time"] = pd.to_numeric(df_clean["dwell_time"], errors="coerce")
    df_clean = df_clean.dropna(subset=["dwell_time"])

    st.line_chart(df_clean[["dwell_time"]])
    
    st.divider()
    
    st.subheader("Interprétation métier")
    
    st.write(f"""
    - Type marchandise : {cargo_type}
    - Pays origine : {origin_country}
    - Volume transitaire : {forwarder_volume}
    
    -> Le conteneur devrait rester environ **{round(prediction,2)} jours**.
    """)