FROM python:3.8-slim

WORKDIR /app

# Instala dependencias necesarias (incluye netcat)
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]