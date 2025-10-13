# run.py
import os
from app import create_app 

# Crea una instancia de la aplicación Flask
app = create_app()

if __name__ == "__main__":
    # La aplicación se ejecuta en modo de desarrollo
    app.run(debug=True)