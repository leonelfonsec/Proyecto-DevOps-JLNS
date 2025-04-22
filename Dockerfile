FROM python:3.11-slim

WORKDIR /app

# Instala dependencias necesarias del sistema
RUN apt-get update && \
    apt-get install -y netcat-openbsd gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia e instala dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Define variable de entorno para evitar problemas con Python buffer
ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "echo 'Starting with DATABASE_URL=$DATABASE_URL'; python run.py"]
