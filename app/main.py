from fastapi import FastAPI, Query
import joblib
import numpy as np
from app.schemas import PredictionResponse
from app.ml.fetch_fire_history import get_fire_count
from app.ml.fetch_live_data import fetch_weather
from app.ml.fetch_ndvi import get_ndvi
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OR use ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = joblib.load("app/ml/model.pkl")

@app.get("/")
def root():
    return {"message": "Wildfire Detection API is Live"}

@app.get("/predict-live", response_model=PredictionResponse)
def predict_from_live_data(
    lat: float = Query(..., description="Latitude of the selected location"),
    lon: float = Query(..., description="Longitude of the selected location")
):
    # 1. Fetch Weather Data
    weather = fetch_weather(lat, lon)
    if not weather:
        return {
            "temperature": None,
            "humidity": None,
            "wind_speed": None,
            "vegetation": None,
            "recent_fires": 0,
            "fire_detected": False,
            "fire_probability": 0.0
        }

    # 2. Fetch NDVI
    ndvi = get_ndvi(lat, lon)
    if ndvi is None:
        ndvi = 0.5

    # 3. Fire history from NASA
    recent_fires = get_fire_count(lat, lon)
    print(f"🔥 NASA Fire Count near ({lat},{lon}):", recent_fires)

    # 4. ML prediction
    features = np.array([[weather["temperature"], weather["humidity"], weather["wind_speed"], ndvi, recent_fires]])
    prediction = model.predict(features.astype(float))[0]
    probability = model.predict_proba(features)[0][1]

    # 5. Return full result
    return {
        "temperature": weather["temperature"],
        "humidity": weather["humidity"],
        "wind_speed": weather["wind_speed"],
        "vegetation": ndvi,
        "recent_fires": recent_fires,
        "fire_detected": bool(prediction),
        "fire_probability": float(probability),
    }