# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Inicializa SQLAlchemy (la librería que maneja la DB)
db = SQLAlchemy()

def create_app():
    # Crea una instancia de la aplicación Flask
    app = Flask(__name__)
    
    # Carga la configuración desde el archivo config.py (donde está la cadena de la DB)
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), '..', 'config.py'))
    
    # Inicializa la base de datos con la app Flask
    db.init_app(app)
    
    # Importar y registrar los Modelos (Objetos de la DB)
    from . import models  
    
    # Importar y registrar las Rutas (Controller - la lógica)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Importar utilidades y crear las tablas
    from .utils import obtener_preguntas_dummy 
    
    with app.app_context():
        # Crea todas las tablas definidas en models.py
        db.create_all() 
        # Carga las preguntas de prueba en la DB 
        obtener_preguntas_dummy() 

    return app