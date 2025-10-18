# config.py

import os
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env (si existe)
load_dotenv() 

class Config:
    # ----------------------------------------------------------------------
    # Configuraciones Generales
    # ----------------------------------------------------------------------
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-muy-dificil'
    DEBUG = True 
    
    # ----------------------------------------------------------------------
    # Configuraciones de la Base de Datos (SQLAlchemy)
    # ----------------------------------------------------------------------
    
    # ¡CONEXIÓN DIRECTA! Esto elimina el riesgo de variables no definidas.
    # Usuario: root, Contraseña: Administrador-1, Nombre de DB: trivia
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:Administrador-1@localhost/trivia' 
            
    # Deshabilita una advertencia de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clave de la API de Pixabay (RF-07)
    PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')
    
    # Configuración para que Flask sepa dónde buscar las plantillas
    TEMPLATES_AUTO_RELOAD = True