from flask import Flask
from .extensions import db, migrate,init_cors
from config import Config

def create_app():
    # Inicialización de la aplicación Flask
    app = Flask(__name__)
    
    # --- CONFIGURACIÓN DE LA APLICACIÓN ---
    
    # Cargar la configuración desde el archivo config.py
    app.config.from_object('config.Config')

    # --- INICIALIZACIÓN DE EXTENSIONES ---
    
    # Inicializar la base de datos (SQLAlchemy)
    db.init_app(app)
    migrate.init_app(app, db)
    init_cors(app)


    # --- REGISTRO DE BLUEPRINTS (RUTAS) ---
    
    # Importar los Blueprints de las rutas (main_bp y admin_bp)
    from .routers import main_bp, admin_bp
    
    # Registrar el Blueprint principal (la página de inicio)
    app.register_blueprint(main_bp)

    # Registrar el Blueprint de administración
    app.register_blueprint(admin_bp)

    # El punto de importación final de modelos es necesario para que db.create_all() funcione
    @app.get("/health")
    def health():
        return {"status": "ok"}
    
    from .cli import register_cli
    register_cli(app)

    with app.app_context():
        
        from . import models 

    return app


