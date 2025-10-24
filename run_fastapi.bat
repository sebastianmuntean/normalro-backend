@echo off
REM Script pentru pornirea backend-ului FastAPI pe Windows

cd /d "%~dp0"

REM Activează virtual environment dacă există
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Instalează dependențele
pip install -r requirements_fastapi.txt

REM Pornește serverul FastAPI
uvicorn anaf_api:app --host 0.0.0.0 --port 8000 --reload

