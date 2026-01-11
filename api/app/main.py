from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import requests, os

# -----------------------------
# Configurações
# -----------------------------
app = FastAPI(title="Flight On Time API")

MODEL_SERVICE_URL = os.getenv("MODEL_SERVICE_URL", "http://model:8000")
WEATHER_SERVICE_URL = os.getenv("WEATHER_SERVICE_URL", "http://weather:8000")

# -----------------------------
# Schemas
# -----------------------------
class PredictionRequest(BaseModel):
    icao_empresa: str
    icao_aerodromo_origem: str
    icao_aerodromo_destino: str
    partida_prevista: datetime
    tempo_voo_estimado_hr: float
    distancia_km: float

class PredictionResponse(BaseModel):
    previsao: str
    probabilidade: float
    threshold_usado: float
    previsao_atraso: int
    probabilidade_atraso: float
    clima: dict

# -----------------------------
# Funções auxiliares
# -----------------------------
def get_weather(origem: str, destino: str, data: datetime):
    """
    Consulta o Weather API para obter dados do clima.
    Retorna dados padrão se houver falha.
    """
    try:
        resp = requests.get(
            f"{WEATHER_SERVICE_URL}/forecast",
            params={
                "origem": origem,
                "destino": destino,
                "data": data.isoformat()
            },
            timeout=5
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        # Fallback caso a API de clima falhe
        return {
            "origem": origem,
            "destino": destino,
            "data": data.isoformat(),
            "condicao": "Desconhecida",
            "temperatura": None,
            "vento": None,
            "error": str(e)
        }

# -----------------------------
# Endpoint /predict
# -----------------------------
@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    # 1️⃣ Consultar o Weather API
    clima = get_weather(
        origem=payload.icao_aerodromo_origem,
        destino=payload.icao_aerodromo_destino,
        data=payload.partida_prevista
    )

    # 2️⃣ Construir payload para o modelo incluindo apenas dados esperados
    model_payload = payload.dict()
    # Serializa datetime para string ISO
    model_payload["partida_prevista"] = model_payload["partida_prevista"].isoformat()

    # 3️⃣ Chamar o serviço de modelo
    try:
        model_resp = requests.post(f"{MODEL_SERVICE_URL}/predict", json=model_payload, timeout=10)
        model_resp.raise_for_status()
        model_result = model_resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao chamar o modelo: {e}")

    # 4️⃣ Garantir que todos os campos do schema existam
    return PredictionResponse(
        previsao=model_result.get("previsao", "Desconhecido"),
        probabilidade=model_result.get("probabilidade", 0.0),
        threshold_usado=model_result.get("threshold_usado", 0.5),
        previsao_atraso=model_result.get("previsao_atraso", 0),
        probabilidade_atraso=model_result.get("probabilidade_atraso", 0.0),
        clima=clima
    )

# -----------------------------
# Health check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}
