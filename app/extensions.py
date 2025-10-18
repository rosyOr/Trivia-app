# Este archivo define las extensiones que se inicializarán en app/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS 

# Creamos las instancias de las extensiones (aún sin inicializar)
db = SQLAlchemy()
migrate = Migrate()

# CORS no necesita una instancia, solo una función de inicialización
def init_cors(app):
    # Esto permite que cualquier frontend (origin="*") acceda a la API
    CORS(app, resources={r"/*": {"origins": "*"}}) 
