"""
Test final cu URL-ul corect ANAF
"""
import requests
import json

print("="*70)
print("TEST ANAF API - URL CORECT")
print("="*70)

anaf_url = "https://webservicesp.anaf.ro/api/PlatitorTvaRest/v9/tva"
test_cui = "37024165"
test_date = "2025-03-01"

print(f"\nURL: {anaf_url}")
print(f"CUI: {test_cui}")
print(f"Date: {test_date}")

try:
    response = requests.post(
        anaf_url,
        json=[{"cui": int(test_cui), "data": test_date}],
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        timeout=10
    )
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n[SUCCESS] ANAF API Response:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        if data.get('found'):
            company = data['found'][0]
            date_generale = company.get('date_generale', {})
            print(f"\n[COMPANY INFO]")
            print(f"  CUI: {date_generale.get('cui')}")
            print(f"  Denumire: {date_generale.get('denumire')}")
            print(f"  Reg Com: {date_generale.get('nrRegCom')}")
            print(f"  Adresa: {date_generale.get('adresa')}")
    else:
        print(f"\n[FAIL] HTTP {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)





