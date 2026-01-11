# Flight On Time System 🚀

[![Python](https://img.shields.io/badge/python-3.12+-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-29.1+-blue)](https://www.docker.com/)
[![Status](https://img.shields.io/badge/status-active-green)]()

Sistema simples para prever se um voo vai chegar **no horário ou atrasado**, integrando **modelo de previsão de voo** com **clima em tempo real**.

---

## 🔹 Funcionalidades

* Previsão de **pontualidade ou atraso** de voos
* Probabilidade associada à previsão
* Dados de clima (temperatura, vento, condição do tempo) no aeroporto de origem
* Fácil de rodar localmente ou via Docker

---

## 🔹 Requisitos

* Docker 29.1.2 ou superior
* Python 3.12+ (opcional, para rodar localmente sem Docker)
* Chave da **OpenWeatherMap**: [https://home.openweathermap.org/api_keys](https://home.openweathermap.org/api_keys)

---

## 🔹 Estrutura do projeto

```text
.
├── api/                # API principal que integra modelo + clima
├── model/              # Serviço do modelo de previsão
├── weather/            # API de clima
├── docker-compose.yml
└── test_services.py
```

---

## 🔹 Configuração

1. Adicione uma API KEY nos arquivos `.env` :

```env
OPENWEATHER_API_KEY=sua_chave_aqui
```

2. Confirme que a chave está ativa na OpenWeatherMap.

---

## 🔹 Rodando com Docker

Suba todos os serviços:

```bash
docker-compose up --build
```

Containers que serão criados:

* `model-api` → Modelo de previsão
* `weather-api` → Clima real
* `flight-api` → API principal integrando tudo

Acesse a documentação Swagger da API principal:
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔹 Endpoints

| Endpoint    | Método | Descrição                                                       |
| ----------- | ------ | --------------------------------------------------------------- |
| `/predict`  | POST   | Retorna previsão de atraso/pontualidade do voo + dados de clima |
| `/forecast` | GET    | Retorna previsão de clima no aeroporto de origem                |
| `/health`   | GET    | Retorna `{ "status": "ok" }` para checagem de saúde da API      |

### Exemplo `/predict` (POST)

**Requisição:**

```json
{
  "icao_empresa": "AZU",
  "icao_aerodromo_origem": "SBRF",
  "icao_aerodromo_destino": "SBRJ",
  "partida_prevista": "2025-11-12T22:30:00",
  "tempo_voo_estimado_hr": 1.2,
  "distancia_km": 50.0
}
```

**Resposta:**

```json
{
  "previsao": "Pontual",
  "probabilidade": 0.345,
  "threshold_usado": 0.5,
  "previsao_atraso": 0,
  "probabilidade_atraso": 0.345,
  "clima": {
    "origem": "SBRF",
    "destino": "SBRJ",
    "data": "2025-11-12T22:30:00",
    "condicao": "céu limpo",
    "temperatura": 25.98,
    "vento": 3.09
  }
}
```

### Exemplo `/forecast` (GET)

**Parâmetros:** `origem`, `destino`, `data`
**Descrição:** Retorna previsão de clima no aeroporto de origem.

### Exemplo `/health` (GET)

**Resposta:**

```json
{
  "status": "ok"
}
```

---

## 🔹 Testes rápidos

Use o script `test_services.py`:

```bash
python test_services.py
```

Ele verifica:

* API principal
* Modelo de ML direto
* Weather API
* Swagger Docs

**Exemplo de saída:**

```
[✅] API principal OK (http://localhost:8000/predict)
[✅] Modelo ML OK (http://localhost:8001/predict)
[✅] Weather API OK (http://localhost:8002/forecast)
[✅] Swagger Docs OK (http://localhost:8000/docs)
```
