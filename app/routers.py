from flask import Blueprint, render_template

# Importamos los modelos necesarios
from app.models.categoria import Categoria
from app.models.dificultad import Dificultad

# Definición de Blueprints
main_bp = Blueprint('main', __name__) 
admin_bp = Blueprint('admin', __name__, url_prefix='/admin') 


# ----------------------------------------------------------------------
# Rutas Principales (main_bp)
# ----------------------------------------------------------------------

@main_bp.route('/')
def index():
    """Ruta principal que muestra la página de inicio."""
    return render_template('home.html')


@main_bp.route('/seleccionar-juego')
def seleccionar_juego():
    """Ruta para la página donde el usuario elige categoría y dificultad."""
    
    # Intenta obtener todas las categorías y dificultades.
    # Si la base de datos está vacía, estas listas serán []
    try:
        categorias = Categoria.query.all()
        dificultades = Dificultad.query.all() 
        
    except Exception as e:
        # En caso de que falle la conexión a la DB o falten tablas
        print(f"Error al cargar categorías/dificultades: {e}")
        categorias = []
        dificultades = []

    return render_template('seleccionar_juego.html',
                           categorias=categorias,
                           dificultades=dificultades)

# ----------------------------------------------------------------------
# Rutas de Administración (admin_bp)
# ----------------------------------------------------------------------

@admin_bp.route('/seed-db')
def seed_db():
    """Carga categorías y dificultades iniciales en la DB."""
    try:
        from app.models.categoria import Categoria
        from app.models.dificultad import Dificultad
        from app.extensions import db

        #Crear las categorías
        categorias_data = [
            "Historia",
            "Ciencia",
            "Cine y TV",
            "Deportes",
        ]
        
        for nombre in categorias_data:
            if not Categoria.query.filter_by(nombre=nombre).first():
                db.session.add(Categoria(nombre=nombre))

        # Crear las dificultades
        dificultades_data = ["Fácil", "Intermedio", "Difícil"]
        
        for nombre in dificultades_data:
            if not Dificultad.query.filter_by(nombre=nombre).first():
                db.session.add(Dificultad(nombre=nombre))

        # Guardar cambios
        db.session.commit()
        return "¡Base de datos cargada con categorías y dificultades iniciales con éxito! ✅"

    except Exception as e:
        db.session.rollback()
        return f"Error al cargar datos iniciales: {e}", 500
