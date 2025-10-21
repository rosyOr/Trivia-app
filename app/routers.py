from flask import Blueprint, render_template

# Definición de Blueprints
# Blueprint de la ruta principal (sin prefijo)
main_bp = Blueprint('main', __name__) 

# Blueprint de la ruta de administración (con prefijo /admin)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin') 

# ----------------------------------------------------------------------
# Rutas Principales (main_bp)
# ----------------------------------------------------------------------

@main_bp.route('/')
def index():
    # Ahora renderizamos el contenido real de la página de inicio (home.html)
    # Este archivo usa 'base.html' como su esqueleto.
    return render_template('home.html')

# ----------------------------------------------------------------------
# Rutas de Administración (admin_bp)
# ----------------------------------------------------------------------

@admin_bp.route('/') # La ruta completa será /admin
def admin_index():
    return "Página de administración. Conexión de código exitosa."

