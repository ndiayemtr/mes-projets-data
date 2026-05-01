from pathlib import Path
import pandas as pd
import joblib
import numpy as np

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "model.pkl")
features = joblib.load(BASE_DIR / "features.pkl")

def prepare_input(data):
    df = pd.DataFrame([data])
    return df.reindex(columns=features, fill_value=0)

def predict_congestion(data, threshold_high=0.5):
    df = prepare_input(data)

    proba = model.predict_proba(df)[0]

    # logique métier
    if proba[2] > threshold_high:
        pred = 2
    elif proba[1] > 0.5:
        pred = 1
    else:
        pred = 0

    return proba, pred