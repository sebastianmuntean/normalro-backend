@echo off
REM Script pentru crearea unui virtual environment curat pentru normalro-backend

echo Creating virtual environment...
python -m venv venv_normalro

echo Activating virtual environment...
call venv_normalro\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements_fastapi.txt

echo.
echo ============================================
echo Virtual environment setup complete!
echo ============================================
echo.
echo To activate the environment, run:
echo     venv_normalro\Scripts\activate.bat
echo.
echo To start the FastAPI server:
echo     uvicorn anaf_api:app --reload
echo.





