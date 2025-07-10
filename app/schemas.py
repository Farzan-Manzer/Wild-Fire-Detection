from pydantic import BaseModel
from typing import Optional

class PredictionResponse(BaseModel):
    temperature: Optional[float]
    humidity: Optional[int]
    wind_speed: Optional[float]
    vegetation: float
    recent_fires: int
    fire_detected: bool
    fire_probability: float
