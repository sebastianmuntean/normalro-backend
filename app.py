from datetime import date, datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
import base64
import os
import random
import re
import string
import requests


# Create Flask app
app = Flask(__name__)

# Configure CORS - echivalent cu express cors()
allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000,https://www.normal.ro,https://normal.ro').split(',')
CORS(app, 
     origins=allowed_origins,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "Accept-Language"],
     supports_credentials=True,
     max_age=3600)


# Tools metadata
TOOLS_METADATA = [
    {"slug": "slug-generator", "titleKey": "tools.slugGenerator.title", "descriptionKey": "tools.slugGenerator.description", "endpoint": "/api/tools/slug-generator", "method": "POST"},
    {"slug": "word-counter", "titleKey": "tools.wordCounter.title", "descriptionKey": "tools.wordCounter.description", "endpoint": "/api/tools/word-counter", "method": "POST"},
    {"slug": "password-generator", "titleKey": "tools.passwordGenerator.title", "descriptionKey": "tools.passwordGenerator.description", "endpoint": "/api/tools/password-generator", "method": "POST"},
    {"slug": "base64-converter", "titleKey": "tools.base64Converter.title", "descriptionKey": "tools.base64Converter.description", "endpoint": "/api/tools/base64-converter", "method": "POST"},
    {"slug": "cnp-generator", "titleKey": "tools.cnpGenerator.title", "descriptionKey": "tools.cnpGenerator.description", "endpoint": "/api/tools/cnp-generator", "method": "POST"}
]

SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>/?"
COUNTY_CODES = {"01": "Alba", "02": "Arad", "03": "Argeș", "04": "Bacău", "05": "Bihor", "06": "Bistrița-Năsăud", "07": "Botoșani", "08": "Brașov", "09": "Brăila", "10": "Buzău", "11": "Caraș-Severin", "12": "Cluj", "13": "Constanța", "14": "Covasna", "15": "Dâmbovița", "16": "Dolj", "17": "Galați", "18": "Gorj", "19": "Harghita", "20": "Hunedoara", "21": "Ialomița", "22": "Iași", "23": "Ilfov", "24": "Maramureș", "25": "Mehedinți", "26": "Mureș", "27": "Neamț", "28": "Olt", "29": "Prahova", "30": "Satu Mare", "31": "Sălaj", "32": "Sibiu", "33": "Suceava", "34": "Teleorman", "35": "Timiș", "36": "Tulcea", "37": "Vaslui", "38": "Vâlcea", "39": "Vrancea", "40": "București", "41": "București - Sector 1", "42": "București - Sector 2", "43": "București - Sector 3", "44": "București - Sector 4", "45": "București - Sector 5", "46": "București - Sector 6", "51": "Călărași", "52": "Giurgiu"}
WEIGHTS = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]


# Helper functions
def slugify(value: str) -> str:
    normalized = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE).strip().lower()
    return re.sub(r"[\s_-]+", "-", normalized)


def analyze_text(value: str) -> dict:
    words = re.findall(r"\b\w+\b", value)
    sentences = [s for s in re.split(r"[.!?]+", value) if s.strip()]
    paragraphs = [p for p in value.splitlines() if p.strip()]
    reading_time_minutes = round(len(words) / 200, 2) if words else 0
    return {"words": len(words), "characters": len(value), "sentences": len(sentences), "paragraphs": len(paragraphs), "estimatedReadingMinutes": reading_time_minutes}


def generate_password(length: int, use_lower: bool, use_upper: bool, use_numbers: bool, use_symbols: bool) -> str:
    char_sets = []
    if use_lower: char_sets.append(string.ascii_lowercase)
    if use_upper: char_sets.append(string.ascii_uppercase)
    if use_numbers: char_sets.append(string.digits)
    if use_symbols: char_sets.append(SYMBOLS)
    if not char_sets: raise ValueError("no_charset_selected")
    pool = "".join(char_sets)
    password_chars = [random.choice(chars) for chars in char_sets]
    remaining = max(length - len(password_chars), 0)
    password_chars.extend(random.choice(pool) for _ in range(remaining))
    random.shuffle(password_chars)
    return "".join(password_chars)


def _random_birth_date() -> date:
    start, end = date(1970, 1, 1), date.today()
    return start + timedelta(days=random.randint(0, (end - start).days))


def _parse_birth_date(raw_value: str) -> date:
    try:
        parsed = datetime.strptime(raw_value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValueError("invalid_birth_date")
    if parsed.year < 1800 or parsed.year > 2099:
        raise ValueError("invalid_birth_date")
    return parsed


def _determine_gender_code(gender: str, birth: date) -> int:
    normalized_gender = gender.lower()
    if birth.year < 1800 or birth.year > 2099: raise ValueError("invalid_birth_date")
    if birth.year <= 1899: return 3 if normalized_gender == "male" else 4
    elif birth.year <= 1999: return 1 if normalized_gender == "male" else 2
    else: return 5 if normalized_gender == "male" else 6


def _generate_serial() -> str:
    return f"{random.randint(1, 999):03d}"


def _compute_control_digit(digits: str) -> str:
    total = sum(int(digit) * weight for digit, weight in zip(digits, WEIGHTS))
    remainder = total % 11
    return "1" if remainder == 10 else str(remainder)


def generate_cnp(gender: str | None, birth_date: date | None, county_code: str | None) -> dict:
    resolved_birth = birth_date or _random_birth_date()
    normalized_gender = gender or random.choice(["male", "female"])
    if normalized_gender not in {"male", "female"}: raise ValueError("invalid_gender")
    if not county_code: county_code = random.choice(list(COUNTY_CODES.keys()))
    if county_code not in COUNTY_CODES: raise ValueError("invalid_county")
    gender_code = _determine_gender_code(normalized_gender, resolved_birth)
    yy, mm, dd = f"{resolved_birth.year % 100:02d}", f"{resolved_birth.month:02d}", f"{resolved_birth.day:02d}"
    serial = _generate_serial()
    partial = f"{gender_code}{yy}{mm}{dd}{county_code}{serial}"
    control = _compute_control_digit(partial)
    return {"cnp": f"{partial}{control}", "details": {"gender": normalized_gender, "birthDate": resolved_birth.isoformat(), "countyCode": county_code, "countyName": COUNTY_CODES[county_code], "serial": serial, "controlDigit": control}}


def _resolve_birth_year(gender_code: str, year_suffix: int) -> tuple[int, str]:
    if gender_code not in {str(i) for i in range(1, 10)}: raise ValueError("invalid_cnp")
    if gender_code in {"1", "2"}: year = 1900 + year_suffix
    elif gender_code in {"3", "4"}: year = 1800 + year_suffix
    else: year = 2000 + year_suffix
    gender_label = "unknown" if gender_code == "9" else ("male" if int(gender_code) % 2 == 1 else "female")
    return year, gender_label


def parse_cnp(cnp_value: str) -> dict:
    if not isinstance(cnp_value, str): raise ValueError("invalid_cnp")
    candidate = cnp_value.strip()
    if len(candidate) != 13 or not candidate.isdigit(): raise ValueError("invalid_cnp")
    gender_code, year_suffix, month, day = candidate[0], int(candidate[1:3]), int(candidate[3:5]), int(candidate[5:7])
    county_code, serial, control_digit = candidate[7:9], candidate[9:12], candidate[12]
    try:
        year, gender_label = _resolve_birth_year(gender_code, year_suffix)
        birth_date = date(year, month, day)
    except ValueError as exc:
        raise ValueError("invalid_cnp") from exc
    if county_code not in COUNTY_CODES: raise ValueError("invalid_cnp")
    expected_control = _compute_control_digit(candidate[:12])
    if expected_control != control_digit: raise ValueError("invalid_cnp")
    return {"cnp": candidate, "details": {"gender": gender_label, "birthDate": birth_date.isoformat(), "countyCode": county_code, "countyName": COUNTY_CODES[county_code], "serial": serial, "controlDigit": control_digit}}


# Routes
@app.route('/')
def home():
    return jsonify({"message": "normalro API", "version": "1.0", "endpoints": ["/api/health", "/api/tools"]})


@app.route('/api/health')
def health_check():
    return jsonify({"status": "ok"})


@app.route('/api/tools')
def list_tools():
    return jsonify({"tools": TOOLS_METADATA})


@app.route('/api/tools/slug-generator', methods=['POST'])
def tool_slug_generator():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    if not text: return jsonify({"error": "text_required"}), 400
    return jsonify({"result": slugify(text)})


@app.route('/api/tools/word-counter', methods=['POST'])
def tool_word_counter():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    if not text.strip(): return jsonify({"error": "text_required"}), 400
    return jsonify({"metrics": analyze_text(text)})


@app.route('/api/tools/password-generator', methods=['POST'])
def tool_password_generator():
    data = request.get_json(silent=True) or {}
    try:
        length = max(4, min(int(data.get("length", 12)), 64))
    except (TypeError, ValueError):
        return jsonify({"error": "invalid_length"}), 400
    use_lower = bool(data.get("lowercase", True))
    use_upper = bool(data.get("uppercase", True))
    use_numbers = bool(data.get("numbers", True))
    use_symbols = bool(data.get("symbols", False))
    try:
        password = generate_password(length, use_lower, use_upper, use_numbers, use_symbols)
    except ValueError as exc:
        if str(exc) == "no_charset_selected": return jsonify({"error": "no_charset_selected"}), 400
        raise
    return jsonify({"password": password, "length": length, "options": {"lowercase": use_lower, "uppercase": use_upper, "numbers": use_numbers, "symbols": use_symbols}})


@app.route('/api/tools/base64-converter', methods=['POST'])
def tool_base64_converter():
    data = request.get_json(silent=True) or {}
    text, mode = data.get("text", ""), data.get("mode", "encode")
    if mode not in {"encode", "decode"}: return jsonify({"error": "invalid_mode"}), 400
    try:
        if mode == "encode":
            return jsonify({"result": base64.b64encode(text.encode("utf-8")).decode("utf-8"), "mode": mode})
        return jsonify({"result": base64.b64decode(text.encode("utf-8"), validate=True).decode("utf-8"), "mode": mode})
    except (ValueError, UnicodeDecodeError):
        return jsonify({"error": "conversion_failed"}), 400


@app.route('/api/tools/cnp-generator', methods=['POST'])
def tool_cnp_generator():
    data = request.get_json(silent=True) or {}
    birth_date = None
    if data.get("birthDate"):
        try:
            birth_date = _parse_birth_date(data.get("birthDate"))
        except ValueError:
            return jsonify({"error": "invalid_birth_date"}), 400
    try:
        result = generate_cnp(data.get("gender"), birth_date, data.get("countyCode"))
    except ValueError as exc:
        if str(exc) in {"invalid_gender", "invalid_county", "invalid_birth_date"}:
            return jsonify({"error": str(exc)}), 400
        raise
    return jsonify(result)


@app.route('/api/tools/cnp-validator', methods=['POST'])
def tool_cnp_validator():
    data = request.get_json(silent=True) or {}
    cnp_value = data.get("cnp", "")
    if not cnp_value: return jsonify({"error": "cnp_required"}), 400
    try:
        return jsonify(parse_cnp(cnp_value))
    except ValueError:
        return jsonify({"error": "invalid_cnp"}), 400


@app.route('/api/anaf/company', methods=['POST'])
def anaf_company_search():
    """Proxy pentru API ANAF - căutare date companie după CUI"""
    data = request.get_json(silent=True) or {}
    cui = data.get("cui", "")
    search_date = data.get("date") or datetime.now().strftime("%Y-%m-%d")
    
    if not cui:
        return jsonify({"error": "cui_required"}), 400
    
    # Curăță CUI-ul
    clean_cui = re.sub(r'[^0-9]', '', str(cui))
    
    if not clean_cui:
        return jsonify({"error": "invalid_cui"}), 400
    
    try:
        # Apel către ANAF (URL corect din codul C# funcțional!)
        anaf_url = "https://webservicesp.anaf.ro/PlatitorTvaRest/api/v9/ws/tva"
        anaf_response = requests.post(
            anaf_url,
            json=[{"cui": int(clean_cui), "data": search_date}],
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if anaf_response.status_code != 200:
            return jsonify({"error": "anaf_service_error"}), 500
        
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
            
            return jsonify({
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
            })
        else:
            return jsonify({"success": False, "error": "CUI nu a fost găsit în ANAF"}), 404
            
    except requests.Timeout:
        return jsonify({"error": "anaf_timeout"}), 504
    except requests.RequestException as e:
        return jsonify({"error": "anaf_connection_error"}), 500
    except Exception as e:
        return jsonify({"error": "server_error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
