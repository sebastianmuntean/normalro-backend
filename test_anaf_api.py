"""
Script de testare pentru ANAF API FastAPI
Testează CORS, endpoint-uri și funcționalitate
"""
import requests
import json
from colorama import init, Fore, Style

init(autoreset=True)

def print_success(msg):
    print(f"{Fore.GREEN}✓ {msg}{Style.RESET_ALL}")

def print_error(msg):
    print(f"{Fore.RED}✗ {msg}{Style.RESET_ALL}")

def print_info(msg):
    print(f"{Fore.CYAN}ℹ {msg}{Style.RESET_ALL}")

def test_local_health():
    """Test health check endpoint local"""
    print_info("Testing local health check...")
    try:
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code == 200:
            print_success(f"Health check OK: {response.json()}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        return False

def test_local_anaf():
    """Test ANAF endpoint local"""
    print_info("Testing local ANAF endpoint...")
    try:
        response = requests.post(
            "http://localhost:8000/api/anaf/company",
            json={"cui": "12345678"},
            headers={"Content-Type": "application/json"}
        )
        print_info(f"Status: {response.status_code}")
        print_info(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print_error(f"ANAF endpoint error: {e}")
        return False

def test_cors_preflight():
    """Test CORS preflight request"""
    print_info("Testing CORS preflight...")
    try:
        response = requests.options(
            "http://localhost:8000/api/anaf/company",
            headers={
                "Origin": "https://www.normal.ro",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
            "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
            "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers"),
        }
        
        print_info(f"CORS Headers: {json.dumps(cors_headers, indent=2)}")
        
        if cors_headers["Access-Control-Allow-Origin"] == "https://www.normal.ro":
            print_success("CORS configured correctly!")
            return True
        else:
            print_error("CORS not configured correctly")
            return False
    except Exception as e:
        print_error(f"CORS test error: {e}")
        return False

def test_production_health(base_url="https://backend.normal.ro"):
    """Test production health check"""
    print_info(f"Testing production health check at {base_url}...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print_success(f"Production health check OK: {response.json()}")
            return True
        else:
            print_error(f"Production health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Production health check error: {e}")
        return False

def test_production_anaf(base_url="https://backend.normal.ro"):
    """Test production ANAF endpoint"""
    print_info(f"Testing production ANAF endpoint at {base_url}...")
    try:
        response = requests.post(
            f"{base_url}/api/anaf/company",
            json={"cui": "12345678"},
            headers={
                "Content-Type": "application/json",
                "Origin": "https://www.normal.ro"
            }
        )
        print_info(f"Status: {response.status_code}")
        print_info(f"CORS Header: {response.headers.get('Access-Control-Allow-Origin')}")
        print_info(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return True
    except Exception as e:
        print_error(f"Production ANAF endpoint error: {e}")
        return False

def test_production_cors(base_url="https://backend.normal.ro"):
    """Test production CORS"""
    print_info(f"Testing production CORS at {base_url}...")
    try:
        response = requests.options(
            f"{base_url}/api/anaf/company",
            headers={
                "Origin": "https://www.normal.ro",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        cors_origin = response.headers.get("Access-Control-Allow-Origin")
        
        if cors_origin == "https://www.normal.ro":
            print_success(f"Production CORS OK: {cors_origin}")
            return True
        else:
            print_error(f"Production CORS failed: {cors_origin}")
            return False
    except Exception as e:
        print_error(f"Production CORS test error: {e}")
        return False

if __name__ == "__main__":
    print(f"\n{Fore.YELLOW}{'='*60}")
    print(f"  ANAF API FastAPI - Test Suite")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    # Test local
    print(f"\n{Fore.YELLOW}--- LOCAL TESTS ---{Style.RESET_ALL}")
    test_local_health()
    test_local_anaf()
    test_cors_preflight()
    
    # Test production (optional)
    print(f"\n{Fore.YELLOW}--- PRODUCTION TESTS ---{Style.RESET_ALL}")
    choice = input("\nDo you want to test production? (y/n): ")
    if choice.lower() == 'y':
        test_production_health()
        test_production_anaf()
        test_production_cors()
    
    print(f"\n{Fore.YELLOW}{'='*60}")
    print(f"  Tests completed!")
    print(f"{'='*60}{Style.RESET_ALL}\n")

