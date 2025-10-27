# 🚀 Quick Start - Trimitere Automată Email

## 📦 Instalare Dependențe

Backend-ul folosește biblioteci Python standard pentru SMTP - nu sunt necesare instalări suplimentare!

Biblioteca `smtplib` este inclusă în Python standard library.

## 🔒 Model de Securitate

**IMPORTANT:** Utilizatorii folosesc **propriile lor credențiale de email** pentru trimitere!

- ✅ **NU** configurezi credențiale pe server (în .env)
- ✅ **NU** stocăm credențialele utilizatorilor pe server
- ✅ Fiecare utilizator introduce propriul email + App Password în frontend
- ✅ Credențialele sunt trimise prin HTTPS direct către SMTP server
- ✅ Opțional, utilizatorul poate salva credențialele criptat în browser (localStorage)

**Beneficii:**
- 🔒 Mai sigur - fiecare user își folosește propriul cont
- ✉️ Mai autentic - emailurile vin de la adresa utilizatorului, nu de la server
- 📊 Fără limite - nu există risc de rate limiting pe un cont unic

## ⚙️ Configurare (1 minut)

### Pasul 1: Pornește Backend

```bash
cd normalro-backend
python app.py
```

**Asta e tot pentru backend!** Nu mai e nevoie de configurare .env pentru email.

### Pasul 2: Utilizatorul își configurează contul (prima dată)

În InvoiceGenerator:

1. Completează o factură
2. Adaugă email-ul clientului în câmpul "Email" (secțiunea Beneficiar)
3. Click pe **"Trimite Email"** (buton albastru mare)
4. În dialog:
   - Introdu **adresa ta de email** (ex: firma.ta@gmail.com)
   - Introdu **App Password** (vezi mai jos cum se generează)
   - Selectează provider: **"Gmail"** (sau Yahoo, Custom)
   - **Opțional:** Bifează "Salvează credențialele" pentru refolosire
5. Click pe **"Trimite Automat"**

✅ Email-ul se trimite automat în ~10 secunde cu PDF-ul atașat!

---

## 🔑 Cum Generezi App Password?

### Pentru Gmail:

1. Mergi la: https://myaccount.google.com/apppasswords
2. Dacă nu vezi opțiunea:
   - Activează 2FA la: https://myaccount.google.com/security
   - Apoi revino la link-ul de mai sus
3. Selectează "Mail" și device-ul tău
4. Click "Generate"
5. Copiază password-ul de 16 caractere (ex: `abcd efgh ijkl mnop`)
6. Folosește acest password în dialog (NU parola ta Gmail normală!)

### Pentru Yahoo:

1. Mergi la: https://login.yahoo.com/account/security
2. Click "Generate app password"
3. Selectează "Mail"
4. Copiază password-ul generat
5. Folosește acest password în dialog

### Pentru Outlook:

- **Nu necesită App Password** - folosește interfața web (nu SMTP automat)
- Metoda manuală: descarcă PDF → deschide Outlook web → atașează manual

### Pentru Custom SMTP:

- Depinde de providerul tău
- Unii (SendGrid, Mailgun) folosesc API Keys
- Alții folosesc parolă normală

---

## 🔍 Verificare Status

### Endpoint de verificare:
```bash
curl http://localhost:5000/api/email/config
```

**Răspuns (returnează providerii disponibili):**
```json
{
  "success": true,
  "providers": [
    {
      "name": "gmail",
      "displayName": "Gmail",
      "host": "smtp.gmail.com",
      "port": 587,
      "requiresAppPassword": true,
      "appPasswordUrl": "https://myaccount.google.com/apppasswords"
    },
    {
      "name": "yahoo",
      "displayName": "Yahoo Mail",
      "host": "smtp.mail.yahoo.com",
      "port": 587,
      "requiresAppPassword": true,
      "appPasswordUrl": "https://login.yahoo.com/account/security"
    },
    {
      "name": "outlook",
      "displayName": "Outlook/Hotmail",
      "host": "smtp-mail.outlook.com",
      "port": 587,
      "requiresAppPassword": false
    },
    {
      "name": "custom",
      "displayName": "Custom SMTP",
      "host": "smtp.gmail.com",
      "port": 587,
      "requiresAppPassword": false
    }
  ]
}
```

---

## 📋 Checklist Configurare

- [ ] Backend pornit (`python app.py`)
- [ ] Test: `curl http://localhost:5000/api/email/config` returnează lista de provideri
- [ ] Utilizatorul și-a generat App Password pentru Gmail/Yahoo
- [ ] Test trimitere email din InvoiceGenerator cu credențialele utilizatorului

---

## 🐛 Probleme Comune

### "Autentificare eșuată" (Gmail/Yahoo)
❌ **Cauză:** Folosești parola normală în loc de App Password
✅ **Soluție:** 
- Pentru Gmail: Generează App Password la https://myaccount.google.com/apppasswords
- Pentru Yahoo: Generează la https://login.yahoo.com/account/security
- **App Password-ul este diferit de parola ta normală!**

### "Lipsesc credențialele de email"
❌ **Cauză:** Ai lăsat goale câmpurile de email sau parolă în dialog
✅ **Soluție:** Completează ambele câmpuri înainte de a apăsa "Trimite Automat"

### Email-ul nu ajunge la destinatar
✅ Verifică folder-ul SPAM/Junk al destinatarului
✅ Verifică că email-ul destinatarului este corect (fără spații)
✅ Verifică "Sent" în contul tău Gmail/Yahoo pentru confirmare că s-a trimis
✅ Unii provideri SMTP au întârzieri de câteva minute

### "Fișierul nu a fost găsit"
❌ **Cauză:** Upload-ul PDF-ului a eșuat sau a expirat (>1 oră)
✅ **Soluție:** Încearcă din nou - procesul e rapid (~10 secunde total)

### Backend nu răspunde
✅ Verifică că backend-ul rulează pe port 5000
✅ Verifică conexiunea la internet
✅ Verifică CORS - frontend trebuie să aibă acces la backend

---

## 🎬 Demo Setup (1 minut!)

```bash
# 1. Pornește backend (fără .env necesar!)
cd normalro-backend
python app.py

# 2. Test în browser
# - Deschide http://localhost:3000/tools/invoice-generator
# - Completează factură + email client
# - Click "Trimite Email"
# - Introdu ADRESA TA de email + App Password
# - Selectează "Gmail"
# - Click "Trimite Automat"
# - ✅ Email trimis în ~10 secunde!
```

**Notă:** Nu mai e nevoie de .env pentru email! Utilizatorii folosesc propriile credențiale.

---

## 💼 Recomandări Producție

1. **Nu include `.env` în Git** (e deja în .gitignore)
2. **Folosește variabile de mediu ale platformei:**
   - Vercel: Settings → Environment Variables
   - Heroku: Config Vars
   - Railway: Variables
3. **Implementează rate limiting:** max 100 emailuri/oră per user
4. **Monitorizează:** logs pentru emailuri trimise/failed
5. **Backup SMTP:** Configurează 2 provideri (primary + fallback)

---

## 📞 Support

Pentru probleme sau întrebări:
- Consultă [EMAIL_SETUP_GUIDE.md](./EMAIL_SETUP_GUIDE.md) pentru detalii complete
- Verifică logs backend-ului pentru erori SMTP
- Testează manual SMTP cu un script Python simplu

---

**Ultima actualizare:** 27 Octombrie 2025
**Versiune:** 1.0

