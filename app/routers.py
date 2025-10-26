from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from sqlalchemy import func, or_ # Importamos 'or_' para futuras lógicas

# Importamos los modelos necesarios
from app.models.categoria import Categoria
from app.models.dificultad import Dificultad
from app.models.pregunta import Pregunta
from app.models.opcion_respuesta import OpcionRespuesta 

from app.models.usuario import Usuario
from app.models.partida import Partida
from app.models.imagen import Imagen 

# Definición de Blueprints
main_bp = Blueprint('main', __name__) 
admin_bp = Blueprint('admin', __name__, url_prefix='/admin') 

# Constantes de Filtrado (Aseguran que solo se vean las categorías acordadas)
CATEGORIAS_A_MOSTRAR = [
    "Historia",
    "Ciencia",
    "Cine y TV",
    "Deportes",
    "Imágenes"  # La categoría especial
]
DIFICULTADES_A_MOSTRAR = ["Fácil", "Intermedio", "Difícil"]

# ----------------------------------------------------------------------
# Lógica Auxiliar de Base de Datos
# ----------------------------------------------------------------------

def _obtener_o_crear_usuario(nombre_usuario):
    """
    Busca un Usuario por nombre; si no existe, lo crea.
    """
    if not nombre_usuario:
        return None
    
    usuario = Usuario.query.filter_by(nombre=nombre_usuario).first()
    
    if not usuario:
        usuario = Usuario(nombre=nombre_usuario)
        db.session.add(usuario)
        # El commit se realiza al guardar la Partida, no aquí.
    
    return usuario


# ----------------------------------------------------------------------
# Rutas Principales (main_bp)
# ----------------------------------------------------------------------

@main_bp.route('/')
def index():
    """Ruta principal que muestra la página de inicio."""
    return render_template('home.html')


@main_bp.route('/seleccionar-juego', methods=['GET'])
def seleccionar_juego():
    """
    Ruta para la página donde el usuario elige categoría y dificultad.
    """
    # 1. Obtener datos del jugador
    nombre_jugador = request.args.get('username') or request.args.get('guest_name')
    es_invitado = request.args.get('guest_name') is not None
    
    # Si el jugador intentó entrar sin nombre, lo devolvemos a casa
    if not nombre_jugador:
        return redirect(url_for('main.index'))

    # Obtener categorías y dificultades filtradas
    try:
        # Filtro de Categorías
        categorias = Categoria.query.filter(
            Categoria.nombre.in_(CATEGORIAS_A_MOSTRAR)
        ).all()
        
        # Filtro de Dificultades
        dificultades = Dificultad.query.filter(
            Dificultad.nombre.in_(DIFICULTADES_A_MOSTRAR)
        ).all()
        
    except Exception as e:
        print(f"Error al cargar categorías/dificultades: {e}")
        categorias = []
        dificultades = []

    return render_template('seleccionar_juego.html',
                           categorias=categorias,
                           dificultades=dificultades,
                           nombre_jugador=nombre_jugador,
                           es_invitado=es_invitado)


@main_bp.route('/jugar', methods=['POST'])
def jugar():
    """
    Inicia una nueva partida, guarda el usuario (si es necesario) 
    y selecciona la primera pregunta.
    """
    # Obtener parámetros del formulario
    nombre_jugador = request.form.get('nombre_jugador')
    categoria_id = request.form.get('categoria_id', type=int)
    dificultad_id = request.form.get('dificultad_id', type=int)
    # Convertir 'True'/'False' de string a booleano
    es_invitado_str = request.form.get('es_invitado')
    es_invitado = es_invitado_str == 'True'
    
    if not categoria_id or not dificultad_id:
        return redirect(url_for('main.seleccionar_juego', nombre_jugador=nombre_jugador))

    # Obtener o Crear Usuario
    usuario = None
    if not es_invitado:
        usuario = _obtener_o_crear_usuario(nombre_jugador)

    # Crear Partida
    nueva_partida = Partida(
        usuario_id=usuario.usuario_id if usuario else None,
        categoria_id=categoria_id,
        dificultad_id=dificultad_id
    )
    db.session.add(nueva_partida)
    
    # Obtener la Categoría y Dificultad
    categoria = Categoria.query.get(categoria_id)
    dificultad = Dificultad.query.get(dificultad_id)

    # Lógica de selección de preguntas
    
    if categoria and categoria.nombre == "Imágenes":
        # === LÓGICA ESPECIAL DE IMÁGENES (A MEJORAR DESPUÉS) ===
        # Por ahora, selecciona una pregunta de una categoría normal para evitar fallos.
        # Esto asegura que la partida inicie aunque no haya lógica de imagen aun.
        otras_categorias_ids = db.session.query(Categoria.categoria_id).filter(
            Categoria.nombre != "Imágenes"
        ).all()
        otras_categorias_ids = [id[0] for id in otras_categorias_ids]

        pregunta_actual = Pregunta.query.filter(
            Pregunta.categoria_id.in_(otras_categorias_ids),
            Pregunta.dificultad_id == dificultad_id
        ).order_by(func.random()).first()
        
    else:
        # Lógica para categorías normales (Trivia API)
        pregunta_actual = Pregunta.query.filter_by(
            categoria_id=categoria_id,
            dificultad_id=dificultad_id
        ).order_by(func.random()).first()

    # Manejo de error si no hay preguntas
    if not pregunta_actual:
        db.session.rollback()
        return f"Error: No hay preguntas disponibles para la selección {categoria.nombre}/{dificultad.nombre}. Por favor, importa más datos.", 404
    
    # Obtener Opciones de Respuesta para la pregunta actual
    opciones = OpcionRespuesta.query.filter_by(pregunta_id=pregunta_actual.pregunta_id).all()

    # Guardar la nueva partida y el usuario (si es nuevo)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar Partida/Usuario: {e}")
        return "Error interno al iniciar el juego.", 500
    
    # Redirigir a la vista del juego con la primera pregunta
    return render_template('jugar.html',
                           partida=nueva_partida,
                           pregunta=pregunta_actual,
                           opciones=opciones,
                           nombre_jugador=nombre_jugador)

# ----------------------------------------------------------------------
# Rutas de Administración (admin_bp) - ¡Asegúrate de que esta función esté!
# ----------------------------------------------------------------------
@admin_bp.route('/seed-db')
def seed_db():
    """Carga las categorías y dificultades iniciales en la DB."""
    try:
        # Importaciones locales para la función
        from app.models.categoria import Categoria
        from app.models.dificultad import Dificultad
        from app.extensions import db

        # Crear las categorías
        categorias_data = [
            "Historia",
            "Ciencia",
            "Cine y TV",
            "Deportes",
            "Imágenes"
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