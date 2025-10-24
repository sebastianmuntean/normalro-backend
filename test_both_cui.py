"""
Test ANAF API pentru ambele CUI-uri - Furnizor și Beneficiar
"""
import requests
import json

print("="*70)
print("COMPARARE ANAF - Furnizor vs Beneficiar")
print("="*70)

anaf_url = "https://webservicesp.anaf.ro/api/PlatitorTvaRest/v9/tva"
test_date = "2025-03-01"

# CUI-urile din imaginea ta
cuis = [
    ("37024165", "FURNIZOR (PRAVALIA SRL)"),
    ("14146589", "BENEFICIAR (TNT COMPUTERS SRL)")
]

for cui, label in cuis:
    print(f"\n{'='*70}")
    print(f"{label}")
    print(f"CUI: {cui}")
    print(f"{'='*70}")
    
    try:
        response = requests.post(
            anaf_url,
            json=[{"cui": int(cui), "data": test_date}],
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('found'):
                company = data['found'][0]
                date_generale = company.get('date_generale', {})
                
                print(f"\n[DATELE RETURNATE DE ANAF]")
                print(f"  CUI: {date_generale.get('cui')}")
                print(f"  Denumire: {date_generale.get('denumire')}")
                print(f"  nrRegCom: '{date_generale.get('nrRegCom')}'")
                print(f"  Adresa: {date_generale.get('adresa')}")
                print(f"  Telefon: {date_generale.get('telefon')}")
                
                # Afișează JSON complet pentru debugging
                print(f"\n[DATE_GENERALE - RAW]")
                print(json.dumps(date_generale, indent=2, ensure_ascii=False))
            else:
                print(f"\n[NOT FOUND] CUI nu a fost găsit în ANAF")
        else:
            print(f"\n[ERROR] Status: {response.status_code}")
            
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {str(e)}")

print("\n" + "="*70)
print("CONCLUZIE:")
print("Verifică dacă nrRegCom este diferit între cele două companii")
print("="*70)

