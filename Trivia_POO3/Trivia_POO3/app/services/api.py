import requests, html

OPENTDB_BASE = "https://opentdb.com/api.php?amount=50"
print(f"Usando OpenTDB API base: {OPENTDB_BASE}")
RATE_SLEEP_SEC = 5  # OpenTDB limita a 1 request / 5s (response_code 5)

def _get_session_token() -> str:
    r = requests.get(f"{OPENTDB_BASE}", params={"command": "request"})
    r.raise_for_status()
    data = r.json()
    
    return data["results"] # token de sesión (vence por inactividad a las 6h)

_get_session_token()