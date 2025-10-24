#!/bin/bash
# Script pentru crearea unui virtual environment curat pentru normalro-backend

echo "Creating virtual environment..."
python3 -m venv venv_normalro

echo "Activating virtual environment..."
source venv_normalro/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements_fastapi.txt

echo ""
echo "============================================"
echo "Virtual environment setup complete!"
echo "============================================"
echo ""
echo "To activate the environment, run:"
echo "    source venv_normalro/bin/activate"
echo ""
echo "To start the FastAPI server:"
echo "    uvicorn anaf_api:app --reload"
echo ""

