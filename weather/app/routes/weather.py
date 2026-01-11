from fastapi import APIRouter, HTTPException
from app.services.weather_service import get_current_weather
from app.models.weather_response import WeatherResponse

router = APIRouter()

@router.get("/current", response_model=WeatherResponse)
def current_weather(city: str):
    try:
        return get_current_weather(city)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
