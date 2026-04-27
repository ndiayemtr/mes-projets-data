from pathlib import Path
import pandas as pd
import joblib

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "model.pkl")

def prepare_input(data):
    return pd.DataFrame([data])

def predict_quality(data):
    df = prepare_input(data)
    
    proba = model.predict_proba(df)[0]
    pred = model.predict(df)[0]
    
    return pred, proba