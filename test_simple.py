"""
Test simplu pentru a vedea dacă requests funcționează
"""
import sys
import os

# Fix encoding pentru Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")

print("Python version:", sys.version)
print("\nTesting imports...")

try:
    import requests
    print("[OK] requests imported successfully")
    print(f"  Version: {requests.__version__}")
except ImportError as e:
    print(f"[FAIL] Failed to import requests: {e}")
    sys.exit(1)

try:
    from fastapi import FastAPI
    print("[OK] fastapi imported successfully")
except ImportError as e:
    print(f"[FAIL] Failed to import fastapi: {e}")
    sys.exit(1)

try:
    from pydantic import BaseModel
    print("[OK] pydantic imported successfully")
except ImportError as e:
    print(f"[FAIL] Failed to import pydantic: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("Testing ANAF API call...")
print("="*50)

try:
    anaf_url = "https://webservicesp.anaf.ro/PlatitorTvaRest/api/v9/ws/tva"
    test_cui = "12345678"
    test_date = "2024-01-01"
    
    print(f"\nCalling ANAF API:")
    print(f"  URL: {anaf_url}")
    print(f"  CUI: {test_cui}")
    print(f"  Date: {test_date}")
    
    response = requests.post(
        anaf_url,
        json=[{"cui": int(test_cui), "data": test_date}],
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    
    print(f"\nResponse:")
    print(f"  Status Code: {response.status_code}")
    print(f"  Content: {response.text[:500]}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n[OK] ANAF API call successful!")
        print(f"  Found: {data.get('found', [])}")
        print(f"  Not Found: {data.get('notfound', [])}")
    else:
        print(f"\n[FAIL] ANAF API returned error: {response.status_code}")
        
except Exception as e:
    print(f"\n[FAIL] Error calling ANAF API:")
    print(f"  Type: {type(e).__name__}")
    print(f"  Message: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)
print("All tests completed!")
print("="*50)

