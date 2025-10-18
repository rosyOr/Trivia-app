import os
from app import create_app, db # Aseguramos importar db

# Llamamos a la función create_app que hemos definido en app/__init__.py
app = create_app()

# Esta función se ejecutará una sola vez para crear las tablas
# basadas en los modelos definidos en app/models.py (ej: User).
with app.app_context():
    # Creamos todas las tablas que no existan en la base de datos
    db.create_all()

# El resto del código inicia el servidor Flask
if __name__ == '__main__':
    app.run(debug=True)