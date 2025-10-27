"""
Script de test pentru funcționalitatea de trimitere email

Acest script testează:
1. Upload fișier temporar
2. Trimitere email cu atașament
3. Ștergere fișier temporar

Utilizare:
    python test_email.py

Asigură-te că:
- Backend-ul rulează pe http://localhost:5000
- Ai configurat SMTP în .env (cel puțin un provider)
"""

import requests
import base64
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Configurare
API_BASE_URL = 'http://localhost:5000'
TEST_EMAIL = input('Introdu email-ul destinatarului pentru test: ').strip()
TEST_PROVIDER = input('Alege provider (gmail/outlook/yahoo/mailto) [gmail]: ').strip() or 'gmail'

def create_test_pdf():
    """Creează un PDF de test simplu"""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # Scrie text în PDF
    p.setFont("Helvetica-Bold", 24)
    p.drawString(100, 750, "FACTURĂ TEST")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 700, "Aceasta este o factură de test pentru Email Service")
    p.drawString(100, 680, f"Data: 27 Octombrie 2025")
    p.drawString(100, 660, f"Serie: TEST | Nr: 001")
    
    p.drawString(100, 600, "Total: 100.00 RON")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer.read()


def test_email_flow():
    """Testează fluxul complet de trimitere email"""
    
    print("\n" + "="*60)
    print("🧪 TEST TRIMITERE EMAIL - FLUX COMPLET")
    print("="*60 + "\n")
    
    # Step 0: Verifică configurația
    print("📋 Step 0: Verificare configurație SMTP...")
    try:
        response = requests.get(f'{API_BASE_URL}/api/email/config')
        config = response.json()
        
        if not config.get('hasAnyProvider'):
            print("❌ NICIUN PROVIDER SMTP CONFIGURAT!")
            print("\n⚠️ Configurează cel puțin un provider în .env:")
            print("   GMAIL_USER=your-email@gmail.com")
            print("   GMAIL_APP_PASSWORD=your-app-password")
            print("\nVezi EMAIL_SETUP_GUIDE.md pentru detalii.")
            return
        
        print(f"✅ Provideri configurați: {', '.join([p['name'] for p in config['providers']])}")
        
        # Verifică dacă providerul selectat e configurat
        configured_names = [p['name'] for p in config['providers']]
        if TEST_PROVIDER not in configured_names and TEST_PROVIDER != 'custom':
            print(f"\n⚠️ Atenție: Providerul '{TEST_PROVIDER}' nu pare configurat.")
            print(f"   Provideri disponibili: {', '.join(configured_names)}")
            
    except Exception as e:
        print(f"❌ Eroare verificare config: {e}")
        return
    
    # Step 1: Creează PDF de test
    print("\n📄 Step 1: Generare PDF de test...")
    try:
        pdf_bytes = create_test_pdf()
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        print(f"✅ PDF generat: {len(pdf_bytes)} bytes")
    except Exception as e:
        print(f"❌ Eroare generare PDF: {e}")
        return
    
    # Step 2: Upload fișier temporar
    print("\n📤 Step 2: Upload PDF pe server...")
    try:
        response = requests.post(
            f'{API_BASE_URL}/api/email/upload-temp-file',
            json={
                'fileBase64': pdf_base64,
                'filename': 'test_invoice.pdf'
            }
        )
        
        if response.status_code != 200:
            print(f"❌ Eroare upload: {response.json()}")
            return
        
        upload_result = response.json()
        file_id = upload_result['fileId']
        print(f"✅ PDF uploadat: {upload_result['filename']}")
        print(f"   File ID: {file_id}")
        print(f"   Size: {upload_result['size']} bytes")
        
    except Exception as e:
        print(f"❌ Eroare upload: {e}")
        return
    
    # Step 3: Trimite email
    print(f"\n📧 Step 3: Trimitere email către {TEST_EMAIL}...")
    try:
        response = requests.post(
            f'{API_BASE_URL}/api/email/send',
            json={
                'provider': TEST_PROVIDER,
                'to': TEST_EMAIL,
                'subject': 'TEST - Factură TEST 001',
                'body': (
                    'Bună ziua,\n\n'
                    'Acesta este un email de test pentru sistemul de facturare.\n\n'
                    'Detalii factură:\n'
                    '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
                    '📄 Serie/Nr: TEST 001\n'
                    '📅 Data: 27 Octombrie 2025\n'
                    '💰 Total: 100.00 RON\n\n'
                    '📎 Factură atașată în PDF.\n\n'
                    'Cu stimă,\n'
                    'Normal.ro Email Service'
                ),
                'fileId': file_id,
                'filename': 'test_invoice.pdf',
                'fromName': 'Normal.ro Test'
            }
        )
        
        if response.status_code != 200:
            error_data = response.json()
            print(f"❌ Eroare trimitere: {error_data.get('error')}")
            print(f"   Status: {response.status_code}")
            
            # Încearcă să ștergi fișierul chiar dacă a fost eroare
            print("\n🗑️ Curățare după eroare...")
            try:
                requests.delete(f'{API_BASE_URL}/api/email/delete-temp-file/{file_id}')
                print("✅ Fișier temporar șters")
            except:
                pass
            return
        
        send_result = response.json()
        print(f"✅ {send_result['message']}")
        
    except Exception as e:
        print(f"❌ Eroare trimitere email: {e}")
        return
    
    # Step 4: Șterge fișier temporar
    print("\n🗑️ Step 4: Ștergere fișier temporar...")
    try:
        response = requests.delete(
            f'{API_BASE_URL}/api/email/delete-temp-file/{file_id}'
        )
        
        if response.status_code != 200:
            print(f"⚠️ Atenție: Fișierul nu a fost șters (se va șterge automat după 1 oră)")
        else:
            print("✅ Fișier temporar șters cu succes")
        
    except Exception as e:
        print(f"⚠️ Eroare ștergere: {e}")
    
    # Success!
    print("\n" + "="*60)
    print("✅ TEST COMPLET - SUCCES!")
    print("="*60)
    print(f"\n📧 Verifică inbox-ul la {TEST_EMAIL}")
    print("   (verifică și folder-ul SPAM dacă nu găsești email-ul)")
    print("\n💡 Dacă testul a reușit, funcționalitatea este complet operațională!")


if __name__ == '__main__':
    # Verifică dependențe
    try:
        import reportlab
    except ImportError:
        print("❌ Lipsește biblioteca 'reportlab' pentru generare PDF")
        print("\nInstalează cu: pip install reportlab")
        print("\nSau folosește un PDF existent și convertește-l în base64.")
        exit(1)
    
    if not TEST_EMAIL:
        print("❌ Email destinatar lipsă!")
        exit(1)
    
    # Rulează testul
    test_email_flow()

