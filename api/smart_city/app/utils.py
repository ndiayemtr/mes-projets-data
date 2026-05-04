from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "model.pkl")

def prepare_input(data):
    df = pd.DataFrame([data])
    return df

def predict_congestion(data, threshold_high=0.5):
    df = prepare_input(data)

    proba = model.predict_proba(df)[0]

    if proba[2] > threshold_high:
        pred = 2
    elif proba[1] > 0.5:
        pred = 1
    else:
        pred = 0

    return {
        "prediction": int(pred),
        "probabilities": {
            "low": float(proba[0]),
            "medium": float(proba[1]),
            "high": float(proba[2])
        }
    }   