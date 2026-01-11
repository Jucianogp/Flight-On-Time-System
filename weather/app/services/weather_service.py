import os
import requests

API_KEY = os.getenv("WEATHER_API_KEY")

def get_current_weather(city: str):
    if not API_KEY:
        raise Exception("API Key não configurada")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception("Erro ao buscar clima")

    data = response.json()

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"]
    }
