from utils import add_time_features, create_lags

import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.title("Prédiction du flux de camions")

model = joblib.load("model.pkl")

df = pd.read_csv("data.csv")

df.rename(columns={
    "hour": "heure",
    "day": "jour_semaine",
    "lag_1": "trafic_heure_precedente",
    "lag_2": "trafic_2h_avant",
    "rolling_mean": "trafic_moyen_recent"
}, inplace=True)


st.write("Aperçu des données")
st.dataframe(df.head())


if st.button("Prédire"):
    
    df_result = df.copy()
    
    # remettre noms techniques pour le modèle
    df_result = df_result.rename(columns={
        "heure": "hour",
        "jour_semaine": "day",
        "trafic_heure_precedente": "lag_1",
        "trafic_2h_avant": "lag_2",
        "trafic_moyen_recent": "rolling_mean"
    })
    
    X = df_result.drop("truck_count", axis=1)
    
    df_result["prediction"] = model.predict(X)
    
    # remettre noms métier
    df_result.rename(columns={
        "hour": "heure",
        "day": "jour_semaine",
        "lag_1": "trafic_heure_precedente",
        "lag_2": "trafic_2h_avant",
        "rolling_mean": "trafic_moyen_recent"
    }, inplace=True)

    # Traduction jours
    jours = {
        0: "Lundi", 1: "Mardi", 2: "Mercredi",
        3: "Jeudi", 4: "Vendredi", 5: "Samedi", 6: "Dimanche"
    }
    
    df_result["jour_semaine"] = df_result["jour_semaine"].map(jours)

    # 📊 Tableau
    st.subheader("📊 Résultats")
    st.dataframe(df_result.head())
    
    # 📈 Graphique
    st.subheader("📈 Réel vs Prédiction")
    st.line_chart(df_result[["truck_count", "prediction"]])
    
    # 📊 KPI
    mae = np.mean(abs(df_result["truck_count"] - df_result["prediction"]))
    
    st.subheader("📊 Indicateurs")

    col1, col2, col3 = st.columns(3)

    col1.metric("Trafic moyen", int(df_result["truck_count"].mean()))
    col2.metric("Trafic max", int(df_result["truck_count"].max()))
    col3.metric("Erreur MAE", round(mae, 2))

    st.write("🔍 Comparaison erreur")
    df_result["erreur"] = abs(df_result["truck_count"] - df_result["prediction"])
    st.dataframe(df_result[["truck_count", "prediction", "erreur"]].head())