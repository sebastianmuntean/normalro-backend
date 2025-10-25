# 🚀 Start FastAPI Server - Quick Commands

## Comandă corectă:

```bash
uvicorn anaf_api:app --reload
```

**Atenție:** Fișierul se numește `anaf_api.py`, nu `api.py`!

## Pași completi:

### 1. Activează virtual environment (dacă ai unul)
```bash
# Windows
venv_normalro\Scripts\activate

# Linux/Mac
source venv_normalro/bin/activate
```

### 2. Pornește serverul
```bash
uvicorn anaf_api:app --reload
```

### 3. Testează
```bash
# Health check
curl http://localhost:8000/api/health

# Test ANAF endpoint
curl -X POST http://localhost:8000/api/anaf/company \
  -H "Content-Type: application/json" \
  -d '{"cui": "37024165", "date": "2025-03-01"}'
```

## Acces Swagger UI:
http://localhost:8000/docs

## Oprire server:
`Ctrl+C` în terminal

## Production (cu workers):
```bash
uvicorn anaf_api:app --host 0.0.0.0 --port 8000 --workers 4
```

## Troubleshooting:

### Error: "Could not import module 'api'"
- ✅ Folosește `anaf_api:app` nu `api:app`

### Error: "ModuleNotFoundError: No module named 'fastapi'"
- ✅ Instalează dependencies: `pip install -r requirements_fastapi.txt`

### Error: Port 8000 already in use
- ✅ Schimbă portul: `uvicorn anaf_api:app --port 8001`
- Sau oprește procesul care folosește portul 8000


