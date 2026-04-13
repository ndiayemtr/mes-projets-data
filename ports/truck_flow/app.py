from pathlib import Path

import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.set_page_config(layout="wide")

st.title("Dashboard - Flux Camions Port")

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "model.pkl")
df = pd.read_csv(BASE_DIR / "data.csv")

# Rename métier
df.rename(columns={
    "hour": "heure",
    "day": "jour_semaine",
    "lag_1": "trafic_heure_precedente",
    "lag_2": "trafic_2h_avant",
    "rolling_mean": "trafic_moyen_recent"
}, inplace=True)

# Filtres utilisateur
st.sidebar.header("Filtres")

jours_list = ["Tous"] + list(df["jour_semaine"].dropna().unique())
jour_filtre = st.sidebar.selectbox("Jour", jours_list)

heure_filtre = st.sidebar.slider("Heure", 0, 23, (0, 23))

# Application filtres
df_filtered = df.copy()

if jour_filtre != "Tous":
    df_filtered = df_filtered[df_filtered["jour_semaine"] == jour_filtre]

df_filtered = df_filtered[
    (df_filtered["heure"] >= heure_filtre[0]) &
    (df_filtered["heure"] <= heure_filtre[1])
]

# Traduction jours
# jours = {
#     0: "Lundi", 1: "Mardi", 2: "Mercredi",
#     3: "Jeudi", 4: "Vendredi", 5: "Samedi", 6: "Dimanche"
# }
# df["jour_semaine"] = df["jour_semaine"].map(jours)

# FONCTION PRÉVISION 24H
def predict_next_24h(df, model):
    
    df_model = df.rename(columns={
        "heure": "hour",
        "jour_semaine": "day",
        "trafic_heure_precedente": "lag_1",
        "trafic_2h_avant": "lag_2",
        "trafic_moyen_recent": "rolling_mean"
    }).copy()
    
    last_row = df_model.iloc[-1:].copy()
    future_preds = []
    
    for i in range(24):
        
        next_row = last_row.copy()
        
        next_row["hour"] = (next_row["hour"] + 1) % 24
        next_row["day"] = (next_row["day"] + (next_row["hour"] == 0)) % 7
        
        next_row["lag_2"] = last_row["lag_1"]
        next_row["lag_1"] = last_row["truck_count"]
        next_row["rolling_mean"] = (next_row["lag_1"] + next_row["lag_2"]) / 2
        
        X_next = next_row.drop("truck_count", axis=1)
        
        pred = model.predict(X_next)[0]
        next_row["truck_count"] = pred
        
        future_preds.append(pred)
        last_row = next_row.copy()
    
    return future_preds

# Bouton prédiction
if st.button("Lancer l'analyse"):
    
    df_result = df_filtered.copy()
    
    # revert pour modèle
    df_model = df_result.rename(columns={
        "heure": "hour",
        "jour_semaine": "day",
        "trafic_heure_precedente": "lag_1",
        "trafic_2h_avant": "lag_2",
        "trafic_moyen_recent": "rolling_mean"
    })
    
    X = df_model.drop("truck_count", axis=1)
    df_result["prediction"] = model.predict(X)
    
    # KPI
    mae = np.mean(abs(df_result["truck_count"] - df_result["prediction"]))
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Trafic moyen", int(df_result["truck_count"].mean()))
    col2.metric("Pic max", int(df_result["truck_count"].max()))
    col3.metric("Erreur MAE", round(mae, 2))
    
    st.divider()
    
    # Graphique principal
    st.subheader("Trafic réel vs prédiction")
    st.line_chart(df_result[["truck_count", "prediction"]])

    st.divider()

    # Prévision future
    st.subheader("Prévision trafic prochaines 24h")

    df_future_input = df_result.drop(columns=["prediction"])
    future_preds = predict_next_24h(df_future_input, model)

    df_future = pd.DataFrame({
        "heure": range(1, 25),
        "prediction": future_preds
    })

    st.line_chart(df_future.set_index("heure"))
    
    st.divider()
    
    # Alertes congestion
    st.subheader("Alertes congestion")
    
    df_result["alerte"] = df_result["prediction"] > 80
    
    alertes = df_result[df_result["alerte"] == True]
    
    if len(alertes) > 0:
        st.error(f"{len(alertes)} périodes à risque détectées")
        st.dataframe(alertes[["heure", "jour_semaine", "prediction"]])
    else:
        st.success("Aucune congestion détectée")
    
    st.divider()
    
    # Tableau final
    st.subheader("Données détaillées")
    st.dataframe(df_result.head(50))