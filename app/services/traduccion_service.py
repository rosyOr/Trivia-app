import re, os
import deepl
from dotenv import load_dotenv

# Carga la clave API desde el archivo .env
load_dotenv()
AUTH_KEY = os.getenv("DEEPL_API_KEY")

# Asegúrate de que la clave exista antes de inicializar el traductor
if not AUTH_KEY:
    # Esto es una parada de emergencia si no se encuentra la clave.
    # Es crucial para evitar errores.
    raise ValueError("La clave DEEPL_API_KEY no se encontró en el archivo .env. Por favor, revisa la configuración.")

translator = deepl.Translator(AUTH_KEY)

def find_dnt_spans(text):
    """
    Identifica tramos de texto (nombres propios, títulos, etc.) que 
    DeepL no debería traducir (Do Not Translate).
    """
    # 1. Palabras entre comillas simples o dobles
    dnt = re.findall(r'(["\'])(.+?)\1', text)
    spans = [m[1] for m in dnt]
    
    # Lista de términos a preservar manualmente
    whitelist = [
        "Call of Duty", "Black Ops II", "Tom Clancy's Rainbow Six Siege", "Skyscraper",
        "The Big Bang Theory", "World of Warcraft", "Pokémon", "Overwatch League",
        "Hobo with a Shotgun", "Panic! At the Disco", "The Beatles", "Frank Ocean",
        "RuneScape", "Harry Potter", "South Park", "Golden Master", "Super Mario Bros.",
        "Neil Hamburger", "The Walking Dead", "Zelda", "Ernő Rubik", "Super Smash Bros.",
        "San Diego Comic-Con", "Dead Rising", "Falcon Heavy", "Overlord",
        "Mario & Sonic at the Olympic Games", "Slipknot", "Muse",
        "Donkey Kong Country", "Homestuck", "M1911", "Commando", "Pompeii"
    ]
    for w in whitelist:
        if w in text:
            spans.append(w)
            
    # 2. Palabras que parecen acrónimos o nombres propios (Capitalización)
    # Patrón: una o más palabras que inician con mayúscula, seguidas por una palabra con mayúscula
    for m in re.finditer(r'\b(?:[A-Z][\w\.'+"'"+r"]+\s+){1,}[A-Z][\w\.'"+r"]+\b", text):
        spans.append(m.group(0))
        
    # Eliminar duplicados manteniendo el orden relativo (o aproximado)
    seen, result = set(), []
    for s in spans:
        if s not in seen:
            seen.add(s)
            result.append(s)
    return result

def mask(text, spans):
    """
    Reemplaza los tramos DNT con marcadores temporales [[DNT_001]].
    """
    for i, s in enumerate(spans, start=1):
        text = text.replace(s, f"[[DNT_{i:03d}]]")
    return text

def translate_with_deepl(text):
    """
    Realiza la traducción usando DeepL, protegiendo los tramos DNT.
    """
    spans = find_dnt_spans(text)
    masked = mask(text, spans)
    
    # 1. Convertir marcadores DNT a etiquetas HTML <keep>
    html = masked
    for i, s in enumerate(spans, start=1):
        # Envolvemos el texto original DNT dentro de las etiquetas <keep>
        html = html.replace(f"[[DNT_{i:03d}]]", f"<keep>{s}</keep>")
        
    # 2. Llamar a la API de DeepL
    result = translator.translate_text(
        html, target_lang="ES",
        tag_handling="html", ignore_tags=["keep"], # DeepL ignora el contenido de <keep>
        preserve_formatting=True
    )
    
    # 3. Eliminar las etiquetas <keep> del texto traducido final
    out = re.sub(r'</?keep>', '', result.text)
    return out

# Esta es la función que espera el ingesta_service.py
def traducir_texto(texto_en: str) -> str:
    """
    Función de fachada (Facade) para ser llamada por el ingesta_service.
    Simplemente llama a la lógica de traducción con DeepL.
    """
    if not texto_en:
        return ""
    
    # La lógica de ingesta espera esta función, que a su vez llama a tu función Deepl
    return translate_with_deepl(texto_en)