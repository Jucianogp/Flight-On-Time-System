import requests
from datetime import datetime

# -----------------------------
# URLs
# -----------------------------
API_URL = "http://localhost:8000"
MODEL_URL = "http://localhost:8001/predict"
WEATHER_URL = "http://localhost:8002/forecast"

# -----------------------------
# Payload 
# -----------------------------
payload = {
    "icao_empresa": "AZU",
    "icao_aerodromo_origem": "SBRF",
    "icao_aerodromo_destino": "SBRJ",
    "partida_prevista": "2025-11-12T22:30:00",
    "tempo_voo_estimado_hr": 1.2,
    "distancia_km": 50.0
}

# -----------------------------
# Função de teste
# -----------------------------
def test_service(name, method, url, **kwargs):
    try:
        r = requests.request(method, url, timeout=5, **kwargs)
        if r.status_code == 200:
            print(f"[✅] {name} OK ({url})")
            if "application/json" in r.headers.get("content-type", ""):
                print("     Resposta:", r.json())
        else:
            print(f"[⚠️] {name} retornou {r.status_code} ({url})")
    except requests.exceptions.RequestException as e:
        print(f"[❌] {name} erro: {e}")

# -----------------------------
# Testes
# -----------------------------
# 1️⃣ API principal (integrada com Weather)
test_service("API principal", "POST", f"{API_URL}/predict", json=payload)

# 2️⃣ Modelo ML direto
test_service("Modelo ML", "POST", MODEL_URL, json=payload)

# 3️⃣ Weather API (forecast real via OpenWeatherMap)
test_service(
    "Weather API", 
    "GET", 
    f"{WEATHER_URL}?origem={payload['icao_aerodromo_origem']}&destino={payload['icao_aerodromo_destino']}&data={payload['partida_prevista']}"
)

# 4️⃣ Swagger Docs da API principal
test_service("Swagger Docs", "GET", f"{API_URL}/docs")
