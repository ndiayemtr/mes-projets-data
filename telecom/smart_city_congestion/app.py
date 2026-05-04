from pathlib import Path
import requests
import streamlit as st
import pandas as pd
import time

def call_api(input_data):
    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=input_data,
            timeout=2
        )
        response.raise_for_status()

        result = response.json()

        return result["probabilities"], result["prediction"]

    except requests.exceptions.Timeout:
        st.error("Timeout API")
    except requests.exceptions.ConnectionError:
        st.error("API non disponible")
    except Exception as e:
        st.error(f"Erreur: {e}")

    return None, None

st.set_page_config(layout="wide")

st.title("🚦 Smart City - Traffic Congestion Dashboard")

# ======================
# LOAD DATA
# ======================
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "data.csv")

weather_map = {
    0: "Clear",
    1: "Rain",
    2: "Storm"
}

zone_map = {
    0: "Residential",
    1: "Business District",
    2: "Highway"
}

df['weather_label'] = df['weather_impact'].round().astype(int).map(weather_map)
df["zone_label"] = df["zone"].map(zone_map)

# ======================
# KPI
# ======================
st.subheader("📊 KPI Globaux")

col1, col2, col3 = st.columns(3)

col1.metric("Congestion High (%)", round((df["congestion_level"]==2).mean()*100,2))
col2.metric("Avg Speed", round(df["speed_efficiency"].mean(),2))
col3.metric("Traffic Intensity", round(df["traffic_intensity"].mean(),2))

st.divider()

# ======================
# FILTERS
# ======================
st.sidebar.header("🔎 Filtres")

zone_filter = st.sidebar.multiselect(
    "Zone",
    df["zone_label"].unique(),
    df["zone_label"].unique()
)

weather_filter = st.sidebar.multiselect(
    "Weather",
    df["weather_label"].unique(),
    df["weather_label"].unique()
)

df_filtered = df[
    (df["zone_label"].isin(zone_filter)) &
    (df["weather_label"].isin(weather_filter))
]

# ======================
# CHARTS
# ======================
st.subheader("📈 Congestion Distribution")

st.bar_chart(df_filtered["congestion_level"].value_counts())

st.subheader("📉 Traffic vs Speed")

st.line_chart(df_filtered[["traffic_intensity", "speed_efficiency"]].head(500))

st.divider()

# ======================
# TEMPS REEL
# ======================
st.subheader("🚨 Alertes Temps Réel")

start = st.button("Lancer surveillance")

placeholder = st.empty()
alert_box = st.empty()

if start:

    for i in range(200):  # nombre d’événements simulés

        row = df.sample(1).iloc[0]

        input_data = {
            "traffic_intensity": row["traffic_intensity"],
            "speed_efficiency": row["speed_efficiency"],
            "peak_traffic": row["peak_traffic"],
            "weather_impact": row["weather_impact"],
            "event_impact": row["event_impact"],
            "brt_pressure": row["brt_pressure"]
        }

        # proba, pred = predict_congestion(input_data, threshold_high=0.5)

        proba, pred = call_api(input_data)

        if proba is None:
            continue

        # affichage données live
        placeholder.dataframe(pd.DataFrame([row]))

        # 🚨 ALERTES
        if pred == 2:
            alert_box.error(f"""
            🚨 ALERTE CONGESTION ÉLEVÉE
            
            Zone : {row['zone_label']}
            Probabilité : {round(proba['high']*100,2)} %
            """)
        elif pred == 1:
            alert_box.warning("Congestion modérée détectée")
        else:
            alert_box.success("Trafic fluide")

        time.sleep(1)  # vitesse du flux

st.divider()
# ======================
# SIMULATION
# ======================
st.sidebar.header("🎯 Simulation")

traffic = st.sidebar.slider("Traffic Intensity", 0.0, 1.0, 0.5)
speed = st.sidebar.slider("Speed Efficiency", 0.0, 1.0, 0.7)
peak = st.sidebar.selectbox("Peak Traffic", [0,1])
weather = st.sidebar.slider("Weather Impact", 0.0, 1.0, 0.2)
event = st.sidebar.slider("Event Impact", 0.0, 1.0, 0.1)
brt = st.sidebar.slider("BRT Pressure", 0.0, 1.0, 0.3)

threshold = st.sidebar.slider("Seuil Congestion High", 0.3, 0.8, 0.5)

if st.sidebar.button("Predict Congestion"):

    input_data = {
        "traffic_intensity": traffic,
        "speed_efficiency": speed,
        "peak_traffic": peak,
        "weather_impact": weather,
        "event_impact": event,
        "brt_pressure": brt
    }

    # proba, pred = predict_congestion(input_data, threshold)

    proba, pred = call_api(input_data)

    if proba is None:
        st.stop()

    st.subheader("🔮 Résultat")

    col1, col2 = st.columns(2)

    col1.metric("Probabilité High", f"{round(proba['high']*100,2)} %")

    if pred == 2:
        col2.error("🚨 Forte congestion")
        st.warning("Action recommandée : régulation trafic / rerouting")
    elif pred == 1:
        col2.warning("⚠️ Congestion modérée")
    else:
        col2.success("✅ Trafic fluide")

    st.divider()

# ======================
# INSIGHTS
# ======================
st.subheader("📌 Insights")

st.write("""
- La congestion est fortement influencée par l'intensité du trafic et la vitesse.
- Les événements et la météo amplifient les perturbations.
- Le modèle permet d’anticiper les situations critiques en temps réel.
""")