#!/bin/bash
# Script pentru pornirea backend-ului FastAPI

cd "$(dirname "$0")"

# Activează virtual environment dacă există
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Instalează dependențele
pip install -r requirements_fastapi.txt

# Pornește serverul FastAPI
uvicorn anaf_api:app --host 0.0.0.0 --port 8000 --reload

