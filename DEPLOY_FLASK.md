# 🚀 Deployment Flask (app.py) pe Backend.normal.ro

## 📋 Ce contine app.py

- ✅ Toate tool-urile existente (slug-generator, word-counter, etc.)
- ✅ Endpoint ANAF `/api/anaf/company`
- ✅ CORS configurat pentru www.normal.ro
- ✅ URL ANAF corectat: `https://webservicesp.anaf.ro/api/PlatitorTvaRest/v9/tva`

---

## 🚀 1. Deployment pe Server

### A. Upload fișiere
```bash
# Din local, upload pe server:
scp app.py user@backend.normal.ro:/var/www/backend.normal.ro/
scp requirements.txt user@backend.normal.ro:/var/www/backend.normal.ro/
```

### B. Pe server - Instalare
```bash
ssh user@backend.normal.ro
cd /var/www/backend.normal.ro

# Creează virtual environment
python3 -m venv venv
source venv/bin/activate

# Instalează dependencies
pip install -r requirements.txt
pip install gunicorn  # Pentru production
```

---

## ⚙️ 2. Configurare Systemd Service

```bash
sudo nano /etc/systemd/system/normalro-backend.service
```

**Conținut:**
```ini
[Unit]
Description=NormalRO Backend Flask API
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/backend.normal.ro
Environment="PATH=/var/www/backend.normal.ro/venv/bin"
Environment="ALLOWED_ORIGINS=http://localhost:3000,https://www.normal.ro,https://normal.ro"

# Flask cu Gunicorn
ExecStart=/var/www/backend.normal.ro/venv/bin/gunicorn app:app \
    --workers 4 \
    --bind 127.0.0.1:5000 \
    --access-logfile /var/log/normalro/access.log \
    --error-logfile /var/log/normalro/error.log \
    --log-level info

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Activează serviciul
```bash
# Creează director logs
sudo mkdir -p /var/log/normalro
sudo chown -R www-data:www-data /var/log/normalro

# Ajustează permisiuni
sudo chown -R www-data:www-data /var/www/backend.normal.ro

# Start service
sudo systemctl daemon-reload
sudo systemctl enable normalro-backend
sudo systemctl start normalro-backend
sudo systemctl status normalro-backend
```

---

## 🌐 3. Configurare Nginx

```bash
sudo nano /etc/nginx/sites-available/backend.normal.ro
```

**Conținut:**
```nginx
# Upstream pentru Flask
upstream flask_backend {
    server 127.0.0.1:5000;
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

    # SSL (certbot)
    ssl_certificate /etc/letsencrypt/live/backend.normal.ro/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/backend.normal.ro/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/backend.normal.ro.access.log;
    error_log /var/log/nginx/backend.normal.ro.error.log;

    client_max_body_size 10M;

    # Root
    location / {
        return 200 '{"status":"ok","service":"NormalRO Backend API"}';
        add_header Content-Type application/json;
    }

    # Toate API endpoint-urile
    location /api/ {
        proxy_pass http://flask_backend/api/;
        
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Flask gestionează CORS - nu adăuga headers aici!
    }

    # Health check
    location /health {
        proxy_pass http://flask_backend/api/health;
        access_log off;
    }
}
```

### Activează și reload Nginx
```bash
sudo ln -s /etc/nginx/sites-available/backend.normal.ro /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🔒 4. SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d backend.normal.ro
```

---

## ✅ 5. Testare

### A. Test local
```bash
curl http://localhost:5000/api/health
```

### B. Test extern
```bash
curl https://backend.normal.ro/api/health
```

### C. Test ANAF
```bash
curl -X POST https://backend.normal.ro/api/anaf/company \
  -H "Content-Type: application/json" \
  -H "Origin: https://www.normal.ro" \
  -d '{"cui": "37024165"}'
```

### D. Test CORS
```bash
curl -H "Origin: https://www.normal.ro" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://backend.normal.ro/api/anaf/company -v
```

Răspuns așteptat:
```
Access-Control-Allow-Origin: https://www.normal.ro
```

### E. Test alte endpoint-uri existente
```bash
# Slug generator
curl -X POST https://backend.normal.ro/api/tools/slug-generator \
  -H "Content-Type: application/json" \
  -d '{"text": "Test String"}'

# Word counter
curl -X POST https://backend.normal.ro/api/tools/word-counter \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world test"}'
```

---

## 📊 6. Monitoring

### View logs
```bash
# Application logs
sudo tail -f /var/log/normalro/error.log
sudo tail -f /var/log/normalro/access.log

# Systemd logs
sudo journalctl -u normalro-backend -f

# Nginx logs
sudo tail -f /var/log/nginx/backend.normal.ro.error.log
```

### Status
```bash
sudo systemctl status normalro-backend
```

### Restart
```bash
sudo systemctl restart normalro-backend
```

---

## 🔄 7. Update Code

Când faci modificări:

```bash
cd /var/www/backend.normal.ro
source venv/bin/activate

# Upload fișierul nou sau pull din git
# scp app.py user@server:/var/www/backend.normal.ro/

# Restart service
sudo systemctl restart normalro-backend
sudo systemctl status normalro-backend
```

---

## 🐛 8. Troubleshooting

### Serviciul nu pornește
```bash
# Logs
sudo journalctl -u normalro-backend -n 50

# Test manual
cd /var/www/backend.normal.ro
source venv/bin/activate
python app.py
```

### 502 Bad Gateway
```bash
# Verifică că Flask rulează
sudo systemctl status normalro-backend
curl http://localhost:5000/api/health
```

### CORS Errors
```bash
# Verifică logs pentru erori
sudo tail -f /var/log/normalro/error.log

# Verifică environment variables
sudo systemctl show normalro-backend | grep ALLOWED_ORIGINS
```

---

## ✅ Checklist

- [ ] app.py uploadat pe server
- [ ] Dependencies instalate
- [ ] Systemd service configurat
- [ ] Service activ și running
- [ ] Nginx configurat
- [ ] SSL certificat instalat
- [ ] Health check funcțional
- [ ] ANAF endpoint funcțional
- [ ] Toate tool-urile funcționează
- [ ] CORS testat și OK
- [ ] Frontend actualizat

---

## 🎉 Next Steps

1. ✅ Backend deployment complet
2. 🔨 Build frontend: `cd _git/normalro-frontend && npm run build`
3. 🚀 Deploy frontend pe www.normal.ro
4. 🧪 Test complet: https://www.normal.ro/tools/invoice-generator

**Un singur backend Flask cu toate endpoint-urile!** 🎯





