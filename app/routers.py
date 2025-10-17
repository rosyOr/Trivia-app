from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import os
import random

# ----------------------------------------------------
# Nota: Usamos TRY/EXCEPT para importar modelos.
# ----------------------------------------------------
try:
    from . import db
    # Modelos a usar (las 8 tablas que hizo tu compañero)
    from .models import Jugador, Partida, Pregunta, Categoria, Dificultad 
    from .utils import obtener_imagen_de_api, generar_preguntas_aleatorias
except ImportError:
    # SIMULACIÓN si la Base de Datos no está lista
    db = None 
    class Jugador:
        def __init__(self, alias): self.alias = alias
    class Partida: pass
    class Categoria: pass
    class Dificultad: pass

# ----------------------------------------------------
# CREACIÓN DEL BLUEPRINT (Módulo Principal)
# ----------------------------------------------------
main = Blueprint('main', __name__)


# ----------------------------------------------------
# RUTA DE INICIO (/) - Conecta con inicio.html
# ----------------------------------------------------
@main.route('/', methods=['GET', 'POST'])
def inicio():
    """
    Ruta para ingresar el alias del jugador y guardarlo en la sesión (RF-01).
    """
    if request.method == 'POST':
        alias = request.form.get('alias').strip()
        
        if not alias:
            return render_template('inicio.html', error="El alias no puede estar vacío.")

        # Lógica de Jugador: Asume que se crea o encuentra un ID
        jugador_id = 999 
            
        session['alias'] = alias
        session['jugador_id'] = jugador_id
        
        # Después de guardar el alias, redirige a /menu
        return redirect(url_for('main.menu'))
    
    # Si es GET, muestra el formulario de inicio
    return render_template('inicio.html')


# ----------------------------------------------------
# RUTA DEL MENÚ DE CONFIGURACIÓN (/menu) - Conecta con menu.html
# ----------------------------------------------------
@main.route('/menu', methods=['GET', 'POST'])
def menu():
    """
    Ruta para que el jugador configure la partida.
    """
    if 'alias' not in session:
        return redirect(url_for('main.inicio'))

    # SIMULACIÓN DE DATOS para menu.html
 
    categorias = [{'id': 1, 'nombre': 'Historia'}, {'id': 2, 'nombre': 'Ciencia'}]
    dificultades = [{'id': 1, 'nombre': 'Fácil'}, {'id': 2, 'nombre': 'Medio'}]
    
    if request.method == 'POST':
        categoria_id = request.form.get('categoria_id')
        nro_preguntas = int(request.form.get('nro_preguntas', 5))
        
        # SIMULACIÓN de preguntas para que la ruta /jugar funcione
        preguntas_simuladas = [
            {'id': 1, 'texto': '¿Capital de Australia?', 'opciones': ['Sídney', 'Melbourne', 'Canberra', 'Perth']},
            {'id': 2, 'texto': '¿Símbolo de Hierro?', 'opciones': ['Au', 'Fe', 'Ag', 'Pb']},
            {'id': 3, 'texto': '¿Quién pintó la Mona Lisa?', 'opciones': ['Miguel Ángel', 'Rafael', 'Da Vinci', 'Picasso']},
        ]
        
        # Guardar el estado inicial de la Partida en la sesión
        session['partida_activa'] = {
            'jugador_id': session['jugador_id'],
            'preguntas': preguntas_simuladas,
            'total_preguntas': nro_preguntas,
            'pregunta_actual_idx': 0,
            'puntaje': 0
        }
        
        return redirect(url_for('main.jugar'))

    return render_template('menu.html', categorias=categorias, dificultades=dificultades)


# ----------------------------------------------------
# RUTA DEL JUEGO (/jugar)
# ----------------------------------------------------
@main.route('/jugar', methods=['GET', 'POST'])
def jugar():
    """
    Maneja la lógica principal del juego y procesa respuestas.
    """
    if 'alias' not in session or 'partida_activa' not in session:
        return redirect(url_for('main.menu'))

    partida_activa = session['partida_activa']
    preguntas_partida = partida_activa['preguntas']
    pregunta_actual_idx = partida_activa['pregunta_actual_idx']

    if request.method == 'POST':
        # Simular avance a la siguiente pregunta
        pregunta_actual_idx += 1
        partida_activa['pregunta_actual_idx'] = pregunta_actual_idx
        session['partida_activa'] = partida_activa 
        
        return redirect(url_for('main.jugar'))

    # Verificar si el juego terminó
    if pregunta_actual_idx >= len(preguntas_partida):
        return redirect(url_for('main.ranking')) 
    
    # Mostrar la pregunta
    pregunta_actual_data = preguntas_partida[pregunta_actual_idx]
    
    return render_template('jugar.html', 
                           pregunta=pregunta_actual_data, 
                           nro_pregunta=pregunta_actual_idx + 1, 
                           total_preguntas=len(preguntas_partida))

# ----------------------------------------------------
# RUTA DE RANKING Y RESULTADOS (/ranking) - Placeholder
# ----------------------------------------------------
@main.route('/ranking')
def ranking():
    """
    Muestra los resultados de la partida y el ranking global (RF-05).
    """
    if 'alias' not in session:
        return redirect(url_for('main.inicio'))
        
    # vista ranking.html
    return render_template('ranking.html')