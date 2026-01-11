# Usar imagem Python slim
FROM python:3.12-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar app e models
COPY app/ ./app/
COPY models/ ./models/

# Expôr a porta
EXPOSE 8001

# Comando para rodar o FastAPI via Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
