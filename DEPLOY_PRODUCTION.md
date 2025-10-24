# 🚀 Deployment pe Backend.normal.ro - Ghid Complet

## 📋 Cerințe

- Server Linux (Ubuntu/Debian recomandat)
- Python 3.8+
- Nginx
- Acces SSH la server
- Domeniu: backend.normal.ro cu DNS configurat

---

## 📁 1. Pregătire Fișiere

### Fișiere de urcat pe server:
```
anaf_api.py
requirements_fastapi.txt
```

### Optional (dacă vrei și Flask):
```
app.py
requirements.txt
```

---

## 🔧 2. Instalare pe Server

### A. Conectare SSH
```bash
ssh user@backend.normal.ro
```

### B. Creează directorul aplicației
```bash
sudo mkdir -p /var/www/backend.normal.ro
sudo chown -R $USER:$USER /var/www/backend.normal.ro
cd /var/www/backend.normal.ro
```

### C. Upload fișiere
Din computerul local:
```bash
# Option 1: SCP
scp anaf_api.py user@backend.normal.ro:/var/www/backend.normal.ro/
scp requirements_fastapi.txt user@backend.normal.ro:/var/www/backend.normal.ro/

# Option 2: Git (recomandat)
# Pe server:
cd /var/www/backend.normal.ro
git clone https://github.com/tau/normalro.git .
cd _git/normalro-backend
```

### D. Instalează Python și pip
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

### E. Creează virtual environment
```bash
cd /var/www/backend.normal.ro
python3 -m venv venv
source venv/bin/activate
```

### F. Instalează dependințe
```bash
pip install --upgrade pip
pip install -r requirements_fastapi.txt

# Instalează și Gunicorn pentru production
pip install gunicorn
```

---

## ⚙️ 3. Configurare Systemd Service

### Creează fișierul service
```bash
sudo nano /etc/systemd/system/normalro-backend.service
```

### Conținut:
```ini
[Unit]
Description=NormalRO Backend FastAPI
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/backend.normal.ro
Environment="PATH=/var/www/backend.normal.ro/venv/bin"

# FastAPI cu Uvicorn și workers
ExecStart=/var/www/backend.normal.ro/venv/bin/gunicorn anaf_api:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000 \
    --access-logfile /var/log/normalro/access.log \
    --error-logfile /var/log/normalro/error.log \
    --log-level info

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Creează director pentru logs
```bash
sudo mkdir -p /var/log/normalro
sudo chown -R www-data:www-data /var/log/normalro
```

### Ajustează permisiuni
```bash
sudo chown -R www-data:www-data /var/www/backend.normal.ro
```

### Activează și pornește serviciul
```bash
sudo systemctl daemon-reload
sudo systemctl enable normalro-backend
sudo systemctl start normalro-backend
sudo systemctl status normalro-backend
```

---

## 🌐 4. Configurare Nginx

### Creează fișierul de configurare
```bash
sudo nano /etc/nginx/sites-available/backend.normal.ro
```

### Conținut:
```nginx
# Upstream pentru FastAPI
upstream fastapi_backend {
    server 127.0.0.1:8000;
    keepalive 64;
}

# Redirect HTTP -> HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name backend.normal.ro;
    
    return 301 https://$server_name$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name backend.normal.ro;

    # SSL Configuration (certbot va crea acestea)
    ssl_certificate /etc/letsencrypt/live/backend.normal.ro/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/backend.normal.ro/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Logging
    access_log /var/log/nginx/backend.normal.ro.access.log;
    error_log /var/log/nginx/backend.normal.ro.error.log;

    # Max body size
    client_max_body_size 10M;

    # Root location
    location / {
        return 200 '{"status":"ok","service":"NormalRO Backend API","docs":"/docs"}';
        add_header Content-Type application/json;
    }

    # Proxy către FastAPI backend
    location /api/ {
        proxy_pass http://fastapi_backend/api/;
        
        # Proxy headers
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # IMPORTANT: Nu adăuga CORS headers aici!
        # FastAPI gestionează CORS
    }

    # Swagger UI (optional, doar pentru development)
    location /docs {
        proxy_pass http://fastapi_backend/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Health check
    location /health {
        proxy_pass http://fastapi_backend/api/health;
        access_log off;
    }
}
```

### Activează site-ul
```bash
sudo ln -s /etc/nginx/sites-available/backend.normal.ro /etc/nginx/sites-enabled/
```

### Test configurație Nginx
```bash
sudo nginx -t
```

### Reload Nginx
```bash
sudo systemctl reload nginx
```

---

## 🔒 5. Configurare SSL (Let's Encrypt)

### Instalează Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### Obține certificat SSL
```bash
sudo certbot --nginx -d backend.normal.ro
```

Urmează instrucțiunile și alege redirect automat HTTP -> HTTPS.

### Verifică renewal automat
```bash
sudo certbot renew --dry-run
```

---

## ✅ 6. Verificare și Testare

### A. Verifică serviciul
```bash
sudo systemctl status normalro-backend
```

### B. Verifică logs
```bash
# Application logs
sudo tail -f /var/log/normalro/error.log
sudo tail -f /var/log/normalro/access.log

# Nginx logs
sudo tail -f /var/log/nginx/backend.normal.ro.error.log

# Systemd logs
sudo journalctl -u normalro-backend -f
```

### C. Test endpoint local
```bash
curl http://localhost:8000/api/health
```

### D. Test endpoint extern
```bash
curl https://backend.normal.ro/api/health
```

### E. Test ANAF endpoint
```bash
curl -X POST https://backend.normal.ro/api/anaf/company \
  -H "Content-Type: application/json" \
  -H "Origin: https://www.normal.ro" \
  -d '{"cui": "37024165", "date": "2025-03-01"}'
```

### F. Test CORS
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
```

---

## 🔧 7. Management și Comenzi Utile

### Restart servicii
```bash
sudo systemctl restart normalro-backend
sudo systemctl reload nginx
```

### Stop servicii
```bash
sudo systemctl stop normalro-backend
```

### View logs în timp real
```bash
sudo journalctl -u normalro-backend -f
```

### Check status
```bash
sudo systemctl status normalro-backend
sudo systemctl status nginx
```

### Test port
```bash
sudo netstat -tlnp | grep 8000
```

---

## 🐛 8. Troubleshooting

### Serviciul nu pornește
```bash
# Verifică logs
sudo journalctl -u normalro-backend -n 50

# Verifică permisiuni
sudo chown -R www-data:www-data /var/www/backend.normal.ro

# Testează manual
cd /var/www/backend.normal.ro
source venv/bin/activate
uvicorn anaf_api:app --host 0.0.0.0 --port 8000
```

### 502 Bad Gateway
- Backend-ul nu rulează: `sudo systemctl start normalro-backend`
- Port greșit în Nginx config
- Verifică: `curl http://localhost:8000/api/health`

### CORS Errors
- Verifică că backend-ul rulează
- Verifică că Nginx NU adaugă duplicate CORS headers
- Verifică logs: `sudo tail -f /var/log/normalro/error.log`

### Permission Denied
```bash
sudo chown -R www-data:www-data /var/www/backend.normal.ro
sudo chmod -R 755 /var/www/backend.normal.ro
```

---

## 📊 9. Monitoring (Optional dar Recomandat)

### Instalează monitoring tools
```bash
sudo apt install htop iotop nethogs -y
```

### Monitor resurse
```bash
htop
```

### Monitor network
```bash
sudo nethogs
```

---

## 🔄 10. Update Application

Când faci modificări în cod:

```bash
cd /var/www/backend.normal.ro
git pull  # sau upload fișiere noi

# Activează venv
source venv/bin/activate

# Reinstalează dependencies (dacă e cazul)
pip install -r requirements_fastapi.txt

# Restart serviciu
sudo systemctl restart normalro-backend

# Verifică status
sudo systemctl status normalro-backend
```

---

## ✅ Checklist Final

- [ ] Python și pip instalate
- [ ] Virtual environment creat
- [ ] Dependencies instalate
- [ ] Systemd service configurat și activ
- [ ] Nginx configurat și rulează
- [ ] SSL certificat instalat
- [ ] Health check funcțional: `curl https://backend.normal.ro/api/health`
- [ ] ANAF endpoint funcțional
- [ ] CORS testat și funcționează
- [ ] Logs monitorizate
- [ ] Frontend actualizat cu `backend.normal.ro`

---

## 🎉 Următorii Pași

După ce backend-ul funcționează:

1. **Testează din browser**: https://backend.normal.ro/docs
2. **Build frontend**: `cd _git/normalro-frontend && npm run build`
3. **Deploy frontend** pe www.normal.ro
4. **Test complet** pe https://www.normal.ro/tools/invoice-generator

---

## 📞 Support

Dacă întâmpini probleme:

1. Verifică logs: `sudo journalctl -u normalro-backend -f`
2. Test local: `curl http://localhost:8000/api/health`
3. Test Nginx: `sudo nginx -t`
4. Verifică DNS: `dig backend.normal.ro`

**Backend gata de producție!** 🚀

