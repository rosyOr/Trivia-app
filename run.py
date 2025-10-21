from dotenv import load_dotenv
load_dotenv() # Carga las variables del archivo .env al inicio

import os
from app import create_app, db
# Importamos modelos para que db.create_all() los detecte
from app import models

# Aseguramos importar los routers o blueprints si fuera necesario

# from app.routers import main_bp # uso si la app usa routers.py

app = create_app()

# Asegura que las tablas se creen antes de iniciar el servidor
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


