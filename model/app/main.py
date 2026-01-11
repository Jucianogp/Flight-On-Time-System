from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI(title="Flight Prediction Model")

# -----------------------------
# Request / Response Schemas
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

# -----------------------------
# Endpoint /predict
# -----------------------------
@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionRequest):
    # Mock de probabilidade do modelo
    probabilidade = round(random.uniform(0.1, 0.9), 3)
    threshold = 0.5
    previsao_atraso = 1 if probabilidade > threshold else 0

    return {
        "previsao": "Atrasado" if previsao_atraso else "Pontual",
        "probabilidade": probabilidade,
        "threshold_usado": threshold,
        "previsao_atraso": previsao_atraso,
        "probabilidade_atraso": probabilidade
    }
