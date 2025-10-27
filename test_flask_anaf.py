"""
Test Flask app.py - verificare endpoint ANAF
"""
import requests
import json

print("="*70)
print("TEST FLASK APP - ANAF ENDPOINT")
print("="*70)

# Asigură-te că Flask rulează pe port 5000
flask_url = "http://localhost:5000/api/anaf/company"
test_cui = "37024165"

print(f"\nFlask URL: {flask_url}")
print(f"Test CUI: {test_cui}")
print("\nTrimite cerere...")

try:
    response = requests.post(
        flask_url,
        json={"cui": test_cui, "date": "2025-03-01"},
        headers={
            "Content-Type": "application/json",
            "Origin": "https://www.normal.ro"
        },
        timeout=30
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"\nCORS Header: {response.headers.get('Access-Control-Allow-Origin', 'NOT FOUND')}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n[SUCCESS] Flask ANAF Response:")
        
        if data.get('success'):
            company_data = data.get('data', {})
            print(f"\n  CUI: {company_data.get('cui')}")
            print(f"  Denumire: {company_data.get('denumire')}")
            print(f"  Nr. Reg. Com: {company_data.get('nrRegCom')}")
            print(f"  Adresa: {company_data.get('adresa')}")
            print(f"  Oras: {company_data.get('oras')}")
            print(f"  Judet: {company_data.get('judet')}")
            print(f"  Platitor TVA: {company_data.get('platitorTVA')}")
            print("\n[OK] ANAF endpoint functioneaza corect in Flask!")
        else:
            print(f"\n[INFO] {data.get('error', 'Unknown error')}")
    else:
        print(f"\n[FAIL] HTTP {response.status_code}")
        try:
            print(f"Error: {response.json()}")
        except:
            print(f"Response: {response.text[:200]}")
        
except requests.exceptions.ConnectionError:
    print("\n[ERROR] Nu pot conecta la Flask!")
    print("Rulează Flask cu: python app.py")
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {str(e)}")

print("\n" + "="*70)
print("Pentru a porni Flask, rulează:")
print("  cd _git/normalro-backend")
print("  python app.py")
print("="*70)





