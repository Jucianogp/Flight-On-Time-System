import os
import requests
from fastapi import FastAPI

app = FastAPI(title="Weather API")

# -----------------------------
# Chave e URL OpenWeatherMap
# -----------------------------
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not OPENWEATHER_API_KEY:
    raise ValueError("É necessário definir a variável OPENWEATHER_API_KEY")

OPENWEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

# Mapeamento ICAO -> Cidade
ICAO_TO_CITY = {
    "SBRF": "Rio de Janeiro",
    "SBRJ": "Rio de Janeiro",
    "SBGR": "São Paulo",
}

@app.get("/forecast")
def forecast(origem: str, destino: str, data: str):
    cidade_origem = ICAO_TO_CITY.get(origem, "Rio de Janeiro")
    params = {
        "q": cidade_origem,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }

    try:
        resp = requests.get(OPENWEATHER_URL, params=params, timeout=5)
        resp.raise_for_status()
        data_weather = resp.json()
        return {
            "origem": origem,
            "destino": destino,
            "data": data,
            "condicao": data_weather["weather"][0]["description"],
            "temperatura": data_weather["main"]["temp"],
            "vento": data_weather["wind"]["speed"]
        }
    except Exception as e:
        return {
            "origem": origem,
            "destino": destino,
            "data": data,
            "condicao": "Desconhecida",
            "temperatura": None,
            "vento": None,
            "error": str(e)
        }

@app.get("/health")
def health():
    return {"status": "ok"}
