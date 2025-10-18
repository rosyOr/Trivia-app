from flask import Flask
# Importamos el módulo de configuración de la raíz para acceder a la clase Config
import config 

from .extensions import db, migrate, init_cors 

# Importamos los Blueprints (rutas) directamente desde routers.py
from .routers import admin_bp 
from .routers import main_bp 

def create_app():
    # Inicialización de la aplicación Flask
    app = Flask(__name__)
    
    # FORZAR LECTURA DE LA CONFIGURACIÓN
    # Leemos la configuración del módulo 'config' de la raíz
    app.config.from_object(config.Config) 
    
    # INICIALIZAR LA BASE DE DATOS y otras extensiones
    db.init_app(app) 
    migrate.init_app(app, db)
    init_cors(app) 

    # REGISTRO DE BLUEPRINTS (Rutas de la aplicación)
    # Registramos las rutas de la sección administrativa y la principal
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(main_bp)
    
    # Comando de salud simple
    @app.route("/health")
    def health():
        return {"status": "ok"}
    
    return app