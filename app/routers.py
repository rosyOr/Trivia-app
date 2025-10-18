from flask import Blueprint, render_template
from .extensions import db
from .models import User 

# Definición de Blueprints
# Blueprint de la ruta principal (sin prefijo)
main_bp = Blueprint('main', __name__) 

# Blueprint de la ruta de administración (con prefijo /admin)
admin_bp = Blueprint('admin', __name__) 


# ----------------------------------------------------------------------
# Rutas Principales (main_bp)
# ----------------------------------------------------------------------

@main_bp.route('/')
def index():
    # Intenta obtener todos los usuarios, esto forzará la conexión a la DB
    try:
        # Esto intenta ejecutar una consulta: SELECT * FROM user
        usuarios = User.query.all()
        # Si funciona, renderiza el template base.html.
        return render_template('base.html', usuarios=usuarios)
    except Exception as e:
        # muestra el error en la pantalla.
        return f"Error CRÍTICO al conectar o leer la base de datos: {e}", 500


# ----------------------------------------------------------------------
# Rutas de Administración (admin_bp)
# ----------------------------------------------------------------------

@admin_bp.route('/admin')
def admin_index():
    return "Página de administración. Conexión de código exitosa."
