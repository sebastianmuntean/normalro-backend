"""
FastAPI backend pentru endpoint-ul ANAF cu CORS corect configurat
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import requests
import re
from typing import Optional

app = FastAPI(
    title="NormalRO ANAF API",
    description="API pentru verificare date companii în ANAF",
    version="1.0.0"
)

# Configure CORS - permite cereri de pe www.normal.ro
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.normal.ro",
        "https://normal.ro",
        "http://localhost:3000",  # pentru development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept-Language"],
    max_age=3600,
)


class ANAFRequest(BaseModel):
    cui: str
    date: Optional[str] = None


class ANAFResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    return {
        "message": "NormalRO ANAF API",
        "version": "1.0.0",
        "endpoints": ["/api/anaf/company"]
    }


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


@app.post("/api/anaf/company")
async def anaf_company_search(request: ANAFRequest):
    """
    Proxy pentru API ANAF - căutare date companie după CUI
    
    Request body:
    {
        "cui": "12345678",
        "date": "2024-01-01"  // optional
    }
    """
    cui = request.cui
    search_date = request.date or datetime.now().strftime("%Y-%m-%d")
    
    if not cui:
        raise HTTPException(status_code=400, detail="cui_required")
    
    # Curăță CUI-ul (elimină RO, spații, caractere non-numerice)
    clean_cui = re.sub(r'[^0-9]', '', str(cui))
    
    if not clean_cui:
        raise HTTPException(status_code=400, detail="invalid_cui")
    
    try:
        # Apel către API-ul ANAF
        anaf_url = "https://webservicesp.anaf.ro/PlatitorTvaRest/api/v9/ws/tva"
        anaf_response = requests.post(
            anaf_url,
            json=[{"cui": int(clean_cui), "data": search_date}],
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if anaf_response.status_code != 200:
            raise HTTPException(status_code=500, detail="anaf_service_error")
        
        anaf_data = anaf_response.json()
        
        # Verifică dacă compania a fost găsită
        if anaf_data.get("found") and len(anaf_data["found"]) > 0:
            company = anaf_data["found"][0]
            date_generale = company.get("date_generale", {})
            adresa_sediu = company.get("adresa_sediu_social", {})
            
            # Construiește adresa completă
            adresa_parts = []
            if adresa_sediu.get("sdenumire_Strada"):
                adresa_parts.append(adresa_sediu["sdenumire_Strada"])
            if adresa_sediu.get("snumar_Strada"):
                adresa_parts.append(f"Nr. {adresa_sediu['snumar_Strada']}")
            if adresa_sediu.get("sdenumire_Localitate"):
                adresa_parts.append(adresa_sediu["sdenumire_Localitate"])
            if adresa_sediu.get("sdenumire_Judet"):
                adresa_parts.append(adresa_sediu["sdenumire_Judet"])
            
            adresa_completa = ", ".join(adresa_parts) if adresa_parts else date_generale.get("adresa", "")
            
            return {
                "success": True,
                "data": {
                    "cui": date_generale.get("cui", clean_cui),
                    "denumire": date_generale.get("denumire", ""),
                    "nrRegCom": date_generale.get("nrRegCom", ""),
                    "adresa": adresa_completa,
                    "oras": adresa_sediu.get("sdenumire_Localitate", ""),
                    "judet": adresa_sediu.get("sdenumire_Judet", ""),
                    "telefon": date_generale.get("telefon", ""),
                    "codPostal": date_generale.get("codPostal", ""),
                    "platitorTVA": company.get("inregistrare_scop_Tva", {}).get("scpTVA", False)
                }
            }
        else:
            return {
                "success": False,
                "error": "CUI nu a fost găsit în ANAF"
            }
            
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="anaf_timeout")
    except requests.RequestException:
        raise HTTPException(status_code=500, detail="anaf_connection_error")
    except Exception as e:
        raise HTTPException(status_code=500, detail="server_error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

