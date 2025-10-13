# config.py

import os
from dotenv import load_dotenv

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASS")
DB_NAME = "trivia_db" 

class Config:
    # Clave secreta de Flask (necesaria para las sesiones)
    SECRET_KEY = os.getenv('SECRET_KEY', 'una-clave-secreta-de-dev')
    
    # Configuración de la Base de Datos (DB)
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{DB_PASSWORD}@localhost:3306/{DB_NAME}'
    
    # Deshabilita una advertencia de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clave de la API de Pixabay (RF-07)
    PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')
    
    # Configuración para que Flask sepa dónde buscar las plantillas
    TEMPLATES_AUTO_RELOAD = True