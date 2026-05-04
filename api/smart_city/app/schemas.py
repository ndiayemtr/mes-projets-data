from pydantic import BaseModel

class TrafficInput(BaseModel):
    traffic_intensity: float
    speed_efficiency: float
    peak_traffic: int
    weather_impact: float
    event_impact: float
    brt_pressure: float