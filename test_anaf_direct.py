"""
Test direct pentru API-ul ANAF cu diferite URL-uri și CUI-uri
"""
import requests
import json

# CUI-uri de test (câteva companii mari din România)
test_cuis = [
    "13328645",  # Dedeman
    "14399840",  # Kaufland
    "1590082",   # OMV Petrom
    "12345678"   # Invalid (pentru test)
]

# URL-uri posibile pentru API ANAF
urls = [
    "https://webservicesp.anaf.ro/PlatitorTvaRest/api/v9/tva",
    "https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/tva",
    "https://webservicesp.anaf.ro/PlatitorTvaRest/api/v7/tva",
    "https://webservicesp.anaf.ro/PlatitorTvaRest/api/v6/tva",
]

print("="*70)
print("TESTING ANAF API - Direct Call")
print("="*70)

for url in urls:
    print(f"\n{'='*70}")
    print(f"Testing URL: {url}")
    print(f"{'='*70}")
    
    for cui in test_cuis[:2]:  # Test doar cu primele 2 CUI-uri
        print(f"\nCUI: {cui}")
        try:
            response = requests.post(
                url,
                json=[{"cui": int(cui), "data": "2024-10-24"}],
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                timeout=10
            )
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  [SUCCESS] Response:")
                    print(f"    Found: {len(data.get('found', []))} companies")
                    print(f"    Not Found: {len(data.get('notfound', []))} companies")
                    if data.get('found'):
                        company = data['found'][0]
                        print(f"    Company: {company.get('date_generale', {}).get('denumire', 'N/A')}")
                except:
                    print(f"  Content: {response.text[:200]}")
            else:
                print(f"  [FAIL] HTTP {response.status_code}")
                print(f"  Content: {response.text[:200]}")
                
        except requests.exceptions.Timeout:
            print(f"  [TIMEOUT] Request took too long")
        except requests.exceptions.RequestException as e:
            print(f"  [ERROR] {type(e).__name__}: {str(e)}")
        except Exception as e:
            print(f"  [ERROR] Unexpected: {type(e).__name__}: {str(e)}")
    
    # Dacă am găsit un URL care funcționează, oprim
    if response.status_code == 200:
        print(f"\n{'='*70}")
        print(f"[SUCCESS] Found working URL: {url}")
        print(f"{'='*70}")
        break

print("\n" + "="*70)
print("Test completed!")
print("="*70)



