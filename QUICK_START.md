# 🚀 Quick Start - FastAPI Backend pentru ANAF

## 1️⃣ Instalare (5 minute)

```bash
cd backend

# Instalează dependențe
pip install -r requirements_fastapi.txt

# Test local
uvicorn anaf_api:app --reload
```

Deschide http://localhost:8000/docs pentru documentația Swagger.

## 2️⃣ Test Local

```bash
# Test health check
curl http://localhost:8000/api/health

# Test ANAF endpoint
curl -X POST http://localhost:8000/api/anaf/company \
  -H "Content-Type: application/json" \
  -d '{"cui": "12345678"}'
```

## 3️⃣ Deploy pe Server

### A. Upload fișierele

```bash
# Copiază fișierele pe server
scp anaf_api.py user@server:/var/www/backend.normal.ro/
scp requirements_fastapi.txt user@server:/var/www/backend.normal.ro/
```

### B. Instalare pe server

```bash
ssh user@server
cd /var/www/backend.normal.ro

# Creează virtual environment
python3 -m venv venv
source venv/bin/activate

# Instalează dependențe
pip install -r requirements_fastapi.txt
```

### C. Configurare systemd

```bash
# Creează serviciu
sudo nano /etc/systemd/system/normalro-anaf.service
```

Conținut:
```ini
[Unit]
Description=NormalRO ANAF FastAPI
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/backend.normal.ro
Environment="PATH=/var/www/backend.normal.ro/venv/bin"
ExecStart=/var/www/backend.normal.ro/venv/bin/uvicorn anaf_api:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

Pornește serviciul:
```bash
sudo systemctl daemon-reload
sudo systemctl enable normalro-anaf
sudo systemctl start normalro-anaf
sudo systemctl status normalro-anaf
```

### D. Configurare Nginx

```bash
# Copiază configurația
sudo cp nginx_backend_normal_ro.conf /etc/nginx/sites-available/backend.normal.ro

# Activează site-ul
sudo ln -s /etc/nginx/sites-available/backend.normal.ro /etc/nginx/sites-enabled/

# Test configurație
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### E. SSL (dacă nu ai deja)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d backend.normal.ro
```

## 4️⃣ Verificare

```bash
# Health check
curl https://backend.normal.ro/api/health

# Test ANAF
curl -X POST https://backend.normal.ro/api/anaf/company \
  -H "Content-Type: application/json" \
  -H "Origin: https://www.normal.ro" \
  -d '{"cui": "12345678"}'

# Test CORS preflight
curl -H "Origin: https://www.normal.ro" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://backend.normal.ro/api/anaf/company -v
```

## 5️⃣ Frontend

Frontend-ul din `_git/normalro-frontend` este deja configurat să folosească `https://backend.normal.ro/api`.

Build și deploy frontend:
```bash
cd _git/normalro-frontend
npm run build
# Deploy build/ pe www.normal.ro
```

## ✅ Done!

Accesează https://www.normal.ro/tools/invoice-generator și testează funcția de căutare CUI.

## 🐛 Probleme?

### CORS Error
- Verifică că backend-ul rulează: `sudo systemctl status normalro-anaf`
- Verifică logs: `sudo journalctl -u normalro-anaf -f`
- Verifică că Nginx nu adaugă duplicate CORS headers

### 502 Bad Gateway
- Backend-ul nu rulează sau nu răspunde pe port 8000
- Verifică: `curl http://localhost:8000/api/health`

### 404 Not Found
- Verifică că endpoint-ul este corect: `/api/anaf/company`
- Verifică configurația Nginx

## 📚 Documentație Completă

Vezi `FASTAPI_DEPLOYMENT.md` pentru detalii complete.

