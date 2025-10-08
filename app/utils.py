# app/utils.py
import requests
import os
from .models import Pregunta, db

# --- Funciones de Utilidad ---

def obtener_imagen_de_api(query: str):
    """
    RF-07: Obtiene una URL de imagen de la API de Pixabay (o similar).
    RNF-03: Maneja errores de conexión.
    """
    API_KEY = os.getenv('PIXABAY_API_KEY')
    if not API_KEY:
        print("ADVERTENCIA: PIXABAY_API_KEY no encontrada en el .env.")
        return None 

    url = "https://pixabay.com/api/"
    params = {
        'key': API_KEY,
        'q': query,
        'image_type': 'photo',
        'per_page': 1,
        'safesearch': True
    }

    try:
        response = requests.get(url, params=params, timeout=5) 
        response.raise_for_status() 
        data = response.json()
        
        if data['hits']:
            return data['hits'][0]['webformatURL']
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de Pixabay: {e}")
        return None


def obtener_preguntas_dummy():
    """
    Función: Proporciona datos iniciales para la tabla Pregunta.
    """
    if Pregunta.query.count() > 0:
        return 

    preguntas_iniciales = [
        Pregunta(texto="¿Cuál es la capital de Australia?", 
                 respuesta_correcta="Canberra", 
                 opciones_falsas="Sídney, Melbourne, Brisbane", 
                 categoria="Geografia", dificultad="Facil"),
                 
        Pregunta(texto="¿Qué elemento químico tiene el símbolo 'Fe'?", 
                 respuesta_correcta="Hierro", 
                 opciones_falsas="Flúor, Fósforo, Ferrita", 
                 categoria="Ciencia", dificultad="Facil"),

        Pregunta(texto="¿En qué año cayó el Muro de Berlín?", 
                 respuesta_correcta="1989", 
                 opciones_falsas="1991, 1985, 1990", 
                 categoria="Historia", dificultad="Medio"),
    ]

    for p in preguntas_iniciales:
        p.imagen_url = obtener_imagen_de_api(p.texto) or 'static/img/default.jpg' 
        db.session.add(p)
    
    db.session.commit()
    print(f"Se cargaron {len(preguntas_iniciales)} preguntas de prueba.")