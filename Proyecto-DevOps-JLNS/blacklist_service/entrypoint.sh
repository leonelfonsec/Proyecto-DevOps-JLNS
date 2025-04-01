#!/bin/sh

# Espera hasta que la base de datos esté disponible
echo "Esperando a que la base de datos esté disponible..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Base de datos disponible, lanzando app..."
exec python run.py
