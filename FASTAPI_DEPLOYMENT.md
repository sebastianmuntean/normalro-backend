# FastAPI Backend - Deployment Guide

## 🚀 Backend FastAPI pentru ANAF API

Backend modern cu FastAPI și CORS corect configurat pentru www.normal.ro.

## 📋 Fișiere create

- `anaf_api.py` - Backend FastAPI principal
- `requirements_fastapi.txt` - Dependențe Python
- `run_fastapi.sh` - Script de pornire pentru Linux
- `run_fastapi.bat` - Script de pornire pentru Windows

## 🔧 Instalare

### 1. Instalare dependențe

```bash
cd backend
pip install -r requirements_fastapi.txt
```

### 2. Test local

```bash
# Linux/Mac
./run_fastapi.sh

# Windows
run_fastapi.bat

# Sau direct
uvicorn anaf_api:app --host 0.0.0.0 --port 8000 --reload
```

Backend-ul va rula pe: http://localhost:8000

### 3. Test endpoint

```bash
curl -X POST http://localhost:8000/api/anaf/company \
  -H "Content-Type: application/json" \
  -d '{"cui": "12345678"}'
```

## 🌐 Deployment pe Server (backend.normal.ro)

### Opțiunea 1: Uvicorn cu systemd (Recomandat)

Creează fișierul `/etc/systemd/system/normalro-anaf.service`:

```ini
[Unit]
Description=NormalRO ANAF FastAPI Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/backend.normal.ro
Environment="PATH=/var/www/backend.normal.ro/venv/bin"
ExecStart=/var/www/backend.normal.ro/venv/bin/uvicorn anaf_api:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Apoi:

```bash
sudo systemctl daemon-reload
sudo systemctl enable normalro-anaf
sudo systemctl start normalro-anaf
sudo systemctl status normalro-anaf
```

### Opțiunea 2: Gunicorn cu Uvicorn workers

```bash
pip install gunicorn
gunicorn anaf_api:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Configurare Nginx

Adaugă în configurația Nginx pentru `backend.normal.ro`:

```nginx
server {
    listen 443 ssl http2;
    server_name backend.normal.ro;

    # SSL config...

    location /api/anaf/ {
        proxy_pass http://localhost:8000/api/anaf/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # CORS preflight cache
        add_header 'Access-Control-Max-Age' 3600;
    }
}
```

Reload Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## 🧪 Test CORS

După deployment, testează CORS:

```bash
curl -H "Origin: https://www.normal.ro" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://backend.normal.ro/api/anaf/company -v
```

Răspunsul ar trebui să conțină:
```
Access-Control-Allow-Origin: https://www.normal.ro
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, Accept-Language
```

## 📊 Verificare funcționare

### 1. Health check
```bash
curl https://backend.normal.ro/api/health
```

Răspuns așteptat: `{"status":"ok"}`

### 2. Test ANAF endpoint
```bash
curl -X POST https://backend.normal.ro/api/anaf/company \
  -H "Content-Type: application/json" \
  -H "Origin: https://www.normal.ro" \
  -d '{"cui": "12345678"}'
```

### 3. Test din browser
Deschide https://www.normal.ro/tools/invoice-generator și încearcă să cauți un CUI.

## 🔍 Logs

### View logs în timp real
```bash
# Systemd
sudo journalctl -u normalro-anaf -f

# Dacă rulezi manual
tail -f /var/log/normalro/anaf.log
```

## 🐛 Troubleshooting

### 1. CORS Errors
- Verifică că `https://www.normal.ro` este în lista `allow_origins`
- Verifică că Nginx nu blochează headerele CORS

### 2. 404 Not Found
- Verifică că endpoint-ul este `/api/anaf/company` (cu `/api` prefix)
- Verifică configurația Nginx proxy_pass

### 3. Connection Refused
- Verifică că serviciul rulează: `sudo systemctl status normalro-anaf`
- Verifică portul: `sudo netstat -tlnp | grep 8000`

### 4. Permission Denied
```bash
sudo chown -R www-data:www-data /var/www/backend.normal.ro
sudo chmod +x /var/www/backend.normal.ro/run_fastapi.sh
```

## 📚 Documentație API

După pornirea serverului, accesează:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔐 Securitate

În producție, consideră:
1. Rate limiting (folosește `slowapi`)
2. API key authentication
3. Request validation strictă
4. Logging complet
5. Monitoring (Prometheus + Grafana)

## 🎯 Next Steps

1. Deploy backend-ul FastAPI pe server
2. Configurează Nginx să facă proxy către FastAPI
3. Testează CORS de pe www.normal.ro
4. Monitorizează logs pentru erori

## ✅ Checklist Deployment

- [ ] Backend FastAPI instalat și rulează pe port 8000
- [ ] Nginx configurat pentru proxy către FastAPI
- [ ] SSL activ pe backend.normal.ro
- [ ] CORS testat și funcțional
- [ ] Frontend actualizat să apeleze backend.normal.ro
- [ ] Logs monitorizate
- [ ] Health check endpoint funcțional

