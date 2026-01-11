# imagem base
FROM python:3.12-slim

# diretório de trabalho
WORKDIR /app

# copiar arquivos de requirements
COPY requirements.txt .

# instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# copiar código da app
COPY . .

# expor porta
EXPOSE 8000

# rodar app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
