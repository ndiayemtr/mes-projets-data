from fastapi import FastAPI
from app.schemas import TrafficInput
from app.utils import predict_congestion

app = FastAPI(
    title="Smart City Congestion API",
    description="Prediction API for urban traffic congestion",
    version="1.0"
)

@app.get("/")
def home():
    return {"message": "Smart City API is running 🚦"}

@app.post("/predict")
def predict(data: TrafficInput):
    result = predict_congestion(data.dict())
    return result