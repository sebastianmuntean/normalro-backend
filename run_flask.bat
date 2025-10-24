@echo off
REM Script pentru pornirea Flask app.py

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask server...
python app.py

