from pathlib import Path

import pandas as pd
import joblib


# Charger modèle 

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "model.pkl")


def prepare_input(data):
    return pd.DataFrame([data])


def predict_churn(data):
    df = prepare_input(data)

    proba = model.predict_proba(df)[0][1]
    pred = int(proba > 0.3)

    return proba, pred
