import requests
import time # Importar time para usar sleep si fuera necesario

OPENTDB_BASE_URL = "https://opentdb.com/"
API_TOKEN_ENDPOINT = f"{OPENTDB_BASE_URL}api_token.php"
RATE_SLEEP_SEC = 5 # OpenTDB limita a 1 request / 5s

def _get_session_token() -> str:
    """
    Solicita un token de sesión a la API de OpenTDB.
    """
    # Usar el endpoint de token y el comando 'request'
    params = {"command": "request"}
    
    # Realizar la solicitud GET al endpoint de tokens
    r = requests.get(API_TOKEN_ENDPOINT, params=params)
    r.raise_for_status() # Verifica si hubo un error HTTP (4xx o 5xx)
    
    data = r.json()
    
    # Verificar el código de respuesta específico de la API (Response Code 0 = Success)
    if data["response_code"] != 0:
        # Aquí puedes manejar errores específicos de la API, como Rate Limiting (código 5)
        raise Exception(f"Error al obtener token de OpenTDB: Código {data['response_code']}")
    
    # El token se devuelve directamente en la clave 'token'
    return data["token"] 

# Ejecución de prueba
try:
    token = _get_session_token()
    print(f"Token de sesión obtenido: {token}")
except Exception as e:
    print(f"Fallo al obtener el token: {e}")