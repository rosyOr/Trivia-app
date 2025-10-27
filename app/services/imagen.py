import requests
from config import UNSPLASH_ACCESS_KEY




def obtener_imagen(pregunta_opciones):
    url = "https://api.unsplash.com/photos/random"
    params = {
        "query": pregunta_opciones,
        "client_id": UNSPLASH_ACCESS_KEY,
        "orientation": "landscape"
    }
    r = requests.get(url, params=params, timeout=10)
    if r.status_code == 200:
        data = r.json()
        return data.get("urls", {}).get("small")  # o "regular" para mayor resolución
    return None