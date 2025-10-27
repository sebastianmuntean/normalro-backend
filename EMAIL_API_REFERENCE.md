# 📧 Email API Reference

## Endpoints Disponibile

### 1. GET `/api/email/config`

**Verifică providerii de email configurați**

#### Request:
```bash
GET http://localhost:5000/api/email/config
```

#### Response:
```json
{
  "success": true,
  "providers": [
    {
      "name": "gmail",
      "host": "smtp.gmail.com",
      "configured": true
    },
    {
      "name": "yahoo",
      "host": "smtp.mail.yahoo.com",
      "configured": true
    }
  ],
  "hasAnyProvider": true
}
```

---

### 2. POST `/api/email/upload-temp-file`

**Uploadează fișier PDF temporar pentru trimitere email**

#### Request:
```bash
POST http://localhost:5000/api/email/upload-temp-file
Content-Type: application/json

{
  "fileBase64": "JVBERi0xLjQKJeLjz9MKMy...",
  "filename": "factura_FAC_001_2025-10-27.pdf"
}
```

#### Response Success:
```json
{
  "success": true,
  "fileId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "filename": "factura_FAC_001_2025-10-27.pdf",
  "size": 45678
}
```

#### Response Error:
```json
{
  "success": false,
  "error": "Format base64 invalid"
}
```

**Notă:** Fișierul este salvat în `temp_files/` și primește un ID unic (UUID).

---

### 3. POST `/api/email/send`

**Trimite email cu PDF atașat**

#### Request:
```bash
POST http://localhost:5000/api/email/send
Content-Type: application/json

{
  "provider": "gmail",
  "to": "client@example.com",
  "subject": "Factura FAC 001 - SC Firma SRL",
  "body": "Bună ziua,\n\nVă transmit factura...",
  "fileId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "filename": "factura_FAC_001_2025-10-27.pdf",
  "fromName": "SC Firma SRL"
}
```

#### Parametri:

| Parametru | Tip | Obligatoriu | Descriere |
|-----------|-----|-------------|-----------|
| `provider` | string | Da | Providerul SMTP: "gmail", "outlook", "yahoo", "mailto" |
| `to` | string | Da | Adresa email destinatar |
| `subject` | string | Da | Subiectul email-ului |
| `body` | string | Da | Corpul email-ului (text simplu) |
| `fileId` | string | Da | ID-ul fișierului uploadat anterior |
| `filename` | string | Nu | Numele fișierului (implicit: "invoice.pdf") |
| `fromName` | string | Nu | Numele afișat ca expeditor (implicit: "Normal.ro Invoice") |

#### Response Success:
```json
{
  "success": true,
  "message": "Email trimis cu succes către client@example.com"
}
```

#### Response Error - Autentificare:
```json
{
  "success": false,
  "error": "Autentificare eșuată. Verifică credențialele SMTP."
}
```
Status: `401 Unauthorized`

#### Response Error - Provider neconfigurat:
```json
{
  "success": false,
  "error": "Providerul \"gmail\" nu este configurat. Setează variabilele de mediu pentru SMTP."
}
```
Status: `500 Internal Server Error`

#### Response Error - Fișier lipsă:
```json
{
  "success": false,
  "error": "Fișierul nu a fost găsit"
}
```
Status: `404 Not Found`

---

### 4. DELETE `/api/email/delete-temp-file/{fileId}`

**Șterge fișierul temporar după trimitere**

#### Request:
```bash
DELETE http://localhost:5000/api/email/delete-temp-file/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

#### Response Success:
```json
{
  "success": true,
  "message": "Fișier șters cu succes"
}
```

#### Response Error:
```json
{
  "success": false,
  "error": "Fișierul nu a fost găsit"
}
```

**Notă:** Fișierul se șterge automat și în caz de eroare la trimitere (în frontend).

---

## 🔄 Flux Complet (Frontend → Backend)

```
┌──────────────┐
│  1. Frontend │ Generează PDF (jsPDF)
│  (React)     │
└──────┬───────┘
       │
       ↓ POST /api/email/upload-temp-file
┌──────────────┐
│  2. Backend  │ Salvează PDF în temp_files/
│  (Flask)     │ Returnează fileId
└──────┬───────┘
       │
       ↓ POST /api/email/send
┌──────────────┐
│  3. Backend  │ Citește PDF din temp_files/
│  (Flask)     │ Trimite email cu PDF atașat (SMTP)
└──────┬───────┘
       │
       ↓ DELETE /api/email/delete-temp-file/{fileId}
┌──────────────┐
│  4. Backend  │ Șterge PDF din temp_files/
│  (Flask)     │
└──────────────┘
       │
       ↓
✅ Email trimis + Fișier șters
```

**Timp total:** 5-10 secunde

---

## 🛡️ Securitate și Limitări

### Limitări Implementate:

1. **Fișiere temporare:**
   - Salvate în `temp_files/` (creat automat)
   - Nume unic cu UUID pentru evitarea coliziunilor
   - Ștergere automată după >1 oră (cleanup periodic)

2. **SMTP:**
   - Conexiune securizată cu STARTTLS
   - Credențiale din variabile de mediu (nu hardcodate)
   - Erori detaliate pentru debugging

3. **Validări:**
   - Verificare existență fișier înainte de trimitere
   - Validare email destinatar (de către SMTP server)
   - Verificare configurație SMTP înainte de trimitere

### Recomandări Producție:

```python
# Adaugă în app.py (înainte de endpoint-uri)

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/email/send', methods=['POST'])
@limiter.limit("10 per minute")  # Max 10 emailuri/minut
def send_email():
    # ... cod existent
```

---

## 📊 Monitoring și Logging

Backend-ul afișează în consolă:

```
✅ Fișier temporar șters: a1b2c3d4-e5f6-7890-abcd-ef1234567890_invoice.pdf
📧 Email trimis către: client@example.com (provider: gmail)
```

Pentru producție, recomand logging în fișiere:

```python
import logging

logging.basicConfig(
    filename='email_service.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

---

## 🧪 Testare Manuală

### Test 1: Upload Fișier
```bash
curl -X POST http://localhost:5000/api/email/upload-temp-file \
  -H "Content-Type: application/json" \
  -d '{
    "fileBase64": "JVBERi0xLjQKJeLjz9MK...",
    "filename": "test.pdf"
  }'
```

### Test 2: Trimitere Email
```bash
curl -X POST http://localhost:5000/api/email/send \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "gmail",
    "to": "test@example.com",
    "subject": "Test Email",
    "body": "Acesta este un test",
    "fileId": "UUID-from-upload",
    "filename": "test.pdf"
  }'
```

### Test 3: Ștergere Fișier
```bash
curl -X DELETE http://localhost:5000/api/email/delete-temp-file/UUID-from-upload
```

---

## 📈 Performanță

### Timpi medii:

- **Upload PDF (1 MB):** ~200-500ms
- **Trimitere email (Gmail):** ~2-5 secunde
- **Ștergere fișier:** ~50ms

**Total end-to-end:** ~5-10 secunde pentru flux complet

### Optimizări:

1. **Cache SMTP connection:** Refolosește conexiunea SMTP pentru multiple emailuri
2. **Async processing:** Folosește task queue (Celery) pentru emailuri în background
3. **CDN pentru PDF:** Uploadează PDF-ul pe CDN și trimite link în email (pentru fișiere mari)

---

## 🔐 Securitate Avansată

### Rate Limiting (Producție):

```python
# Instalează: pip install Flask-Limiter
from flask_limiter import Limiter

limiter = Limiter(app=app, key_func=get_remote_address)

@app.route('/api/email/send', methods=['POST'])
@limiter.limit("50 per day")  # Max 50 emailuri/zi per IP
def send_email():
    # ... cod existent
```

### Validare Email Destinatar:

```python
import re

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# În endpoint:
if not is_valid_email(to_email):
    return jsonify({'error': 'Email invalid'}), 400
```

### Sanitizare Filename:

```python
import os

def sanitize_filename(filename):
    # Permite doar caractere sigure
    return re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

# În endpoint:
filename = sanitize_filename(data.get('filename', 'invoice.pdf'))
```

---

**Creat:** 27 Octombrie 2025
**Versiune:** 1.0
**API Version:** 1.0

