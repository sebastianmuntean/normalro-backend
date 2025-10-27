# 📧 Ghid Configurare Trimitere Automată Email

## 🎯 Scop

Acest ghid explică cum să configurezi backend-ul pentru trimitere automată de emailuri cu facturi PDF atașate.

## 🔧 Configurare SMTP

### 1️⃣ Gmail (Recomandat)

Gmail necesită un **App Password** (nu parola normală pentru securitate sporită).

#### Pași:
1. Mergi la [Google Account Security](https://myaccount.google.com/security)
2. Activează **"2-Step Verification"** (dacă nu e deja activat)
3. Caută **"App passwords"** în search
4. Generează un App Password nou pentru **"Mail"**
5. Copiază password-ul de 16 caractere generat

#### Variabile .env:
```bash
GMAIL_USER=adresa-ta@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
```

**Atenție:** App Password-ul este diferit de parola ta Gmail normală!

---

### 2️⃣ Outlook/Hotmail

Outlook folosește parola normală a contului.

#### Variabile .env:
```bash
OUTLOOK_USER=adresa-ta@outlook.com
OUTLOOK_PASSWORD=parola-ta-normala
```

**Notă:** Dacă ai 2FA activat, poate fi nevoie de App Password similar cu Gmail.

---

### 3️⃣ Yahoo Mail

Yahoo necesită un **App Password** (similar cu Gmail).

#### Pași:
1. Mergi la [Yahoo Account Security](https://login.yahoo.com/account/security)
2. Click pe **"Generate app password"**
3. Selectează **"Mail"** ca aplicație
4. Copiază password-ul generat

#### Variabile .env:
```bash
YAHOO_USER=adresa-ta@yahoo.com
YAHOO_APP_PASSWORD=password-generat-de-yahoo
```

---

### 4️⃣ Custom SMTP Provider

Pentru alți provideri (SendGrid, Mailgun, SMTP propriu de firmă, etc.):

#### Variabile .env:
```bash
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASSWORD=parola-sau-api-key
```

**Provideri populari:**

| Provider | SMTP Host | Port | Note |
|----------|-----------|------|------|
| SendGrid | smtp.sendgrid.net | 587 | Folosește API Key ca password |
| Mailgun | smtp.mailgun.org | 587 | Folosește credențiale SMTP din dashboard |
| Amazon SES | email-smtp.region.amazonaws.com | 587 | Generează SMTP credentials în console |
| Office 365 Business | smtp.office365.com | 587 | Folosește adresa Office 365 |

---

## 📝 Exemplu Fișier .env Complet

```bash
# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://www.normal.ro,https://normal.ro

# Email - Gmail (recomandat pentru teste)
GMAIL_USER=firma.ta@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop

# Email - Outlook (opțional)
OUTLOOK_USER=firma.ta@outlook.com
OUTLOOK_PASSWORD=parola123

# Email - Yahoo (opțional)
YAHOO_USER=firma.ta@yahoo.com
YAHOO_APP_PASSWORD=yahoo-app-pass

# Email - Custom SMTP (opțional)
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.abc123xyz...

# Server
PORT=5000
```

---

## ✅ Verificare Configurație

După configurare, verifică dacă providerul funcționează:

### Endpoint de verificare:
```bash
GET http://localhost:5000/api/email/config
```

**Răspuns așteptat:**
```json
{
  "success": true,
  "providers": [
    {
      "name": "gmail",
      "host": "smtp.gmail.com",
      "configured": true
    }
  ],
  "hasAnyProvider": true
}
```

---

## 🚀 Utilizare în Frontend

După configurare, utilizatorii pot:

1. ✅ Completează factura în InvoiceGenerator
2. ✅ Click pe butonul **"Trimite Email"**
3. ✅ Selectează providerul (Gmail, Yahoo, Custom SMTP)
4. ✅ Click pe **"Trimite Automat"**

**Fluxul automat:**
- PDF-ul se generează automat (fără descărcare)
- Se uploadează temporar pe server
- Se trimite email-ul cu PDF atașat
- Se șterge automat fișierul de pe server

**Total timp:** ~5-10 secunde pentru tot procesul!

---

## 🔒 Securitate

### Best Practices:

1. **Nu include fișierul `.env` în Git!** (e deja în .gitignore)
2. **Folosește App Passwords**, nu parole normale
3. **Rotește periodic App Passwords** (la 6 luni)
4. **Pentru producție:** Folosește variabile de mediu ale serverului (Vercel Env Vars, Heroku Config Vars, etc.)
5. **Rate limiting:** Implementează limite de trimitere (ex: 100 emailuri/zi) pentru a preveni abuzul

### Fișiere temporare:

- Fișierele PDF sunt salvate în `temp_files/`
- Se șterg automat după trimitere (success sau fail)
- Curățare automată: fișiere vechi de >1 oră sunt șterse automat
- Numele fișierelor folosesc UUID-uri unice pentru securitate

---

## 🐛 Troubleshooting

### Eroare: "Autentificare eșuată"
- ✅ Verifică că folosești **App Password** (nu parola normală) pentru Gmail/Yahoo
- ✅ Verifică că adresa email și parola sunt corecte
- ✅ Verifică că ai 2FA activat pentru Gmail

### Eroare: "Provider nu este configurat"
- ✅ Verifică că ai setat variabilele în `.env`
- ✅ Restart backend după modificarea `.env`
- ✅ Verifică că numele variabilelor sunt corecte (GMAIL_USER, nu GMAIL_EMAIL)

### Eroare: "Eroare SMTP: Connection timeout"
- ✅ Verifică conexiunea la internet
- ✅ Verifică că portul 587 nu este blocat de firewall
- ✅ Unii provideri ISP blochează portul 587 - încearcă portul 465 sau 2525

### Email-ul nu ajunge
- ✅ Verifică folder-ul SPAM/Junk al destinatarului
- ✅ Verifică că email-ul destinatarului este corect
- ✅ Pentru Gmail: verifică "Sent" în contul tău Gmail

---

## 📚 Resurse Utile

- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
- [Yahoo App Passwords](https://help.yahoo.com/kb/generate-third-party-passwords-sln15241.html)
- [SendGrid SMTP Guide](https://docs.sendgrid.com/for-developers/sending-email/integrating-with-the-smtp-api)
- [Mailgun SMTP Guide](https://documentation.mailgun.com/en/latest/user_manual.html#sending-via-smtp)

---

## 💡 Recomandări

### Pentru Dezvoltare/Teste:
- Folosește **Gmail** (simplu, gratuit, 500 emailuri/zi)

### Pentru Producție:
- **SendGrid** (gratuit până la 100 emailuri/zi, apoi paid)
- **Mailgun** (gratuit până la 5,000 emailuri/lună)
- **Amazon SES** (foarte ieftin, 0.10$/1000 emailuri)

### Pentru Firme:
- **Office 365 Business** SMTP (dacă ai deja abonament)
- **Google Workspace** SMTP (dacă ai deja abonament)

---

**Creat:** 27 Octombrie 2025
**Versiune:** 1.0

