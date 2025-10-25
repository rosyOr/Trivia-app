# controllers/trivia_bp.py
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models import Pregunta, OpcionRespuesta, Categoria, Dificultad, Partida, Jugador, db
from datetime import datetime
import random

trivia_bp = Blueprint("trivia_bp", __name__)

# iniciar partida 
@trivia_bp.route("/empezar", methods=["GET", "POST"])
def empezar():
    
    # para que empiece la sesion vacia por si sale el mensaje de no hay preguntas disponibles
    session.pop("preguntas_ids", None)
    session.pop("indice_actual", None)
    session.pop("score", None)



    if request.method == "POST":
        dificultad_id = int(request.form.get("dificultad_id", 1))
        categoria_ids = request.form.getlist("categorias")  

        # selecciona preguntas según dificultad/categoría
        query = Pregunta.query.filter_by(dificultad_id=dificultad_id)
        if categoria_ids:
            query = query.filter(Pregunta.categoria_id.in_(categoria_ids))
        preguntas = query.order_by(db.func.rand()).limit(10).all()

        if not preguntas:
            flash("No hay preguntas disponibles para la configuracion puesta.", "warning")
            return redirect(url_for("trivia_bp.empezar")) 

        # guarda la sesion
        session["preguntas_ids"] = [p.pregunta_id for p in preguntas]
        session["indice_actual"] = 0
        session["score"] = 0
        session["start_time"] = datetime.utcnow().timestamp()
        session["dificultad_id"] = dificultad_id
        session["categoria_ids"] = categoria_ids

        return redirect(url_for("trivia_bp.trivia"))

    # GET: muestra formulario de selección de dificultad/categoría
    dificultades = Dificultad.query.all()
    categorias = Categoria.query.all()

    dificultades_desordenadas = [
    {'dificultad_id': 3, 'nombre': 'Facil'},
    {'dificultad_id': 2, 'nombre': 'Media'},
    {'dificultad_id': 1, 'nombre': 'Dificil'}
]

    



    return render_template("trivia_empezar.html", dificultades=dificultades_desordenadas, categorias=categorias)


# partida de trivia creada
@trivia_bp.route("/partida", methods=["GET"])
def trivia():
    #  verifica si hay una sesion de juego activa
    if "preguntas_ids" not in session:
        return redirect(url_for("trivia_bp.start"))

    indice = session.get("indice_actual", 0)
    preguntas_ids = session["preguntas_ids"]

    #  si ya no hay mas preguntas, termina la partida 
    if indice >= len(preguntas_ids):
        return redirect(url_for("trivia_bp.fin_partida"))

    pregunta_id = preguntas_ids[indice]
    pregunta = Pregunta.query.get(pregunta_id)
    opciones = list(OpcionRespuesta.query.filter_by(pregunta_id=pregunta_id).all())

    # mecla las opciones para que no salga la correcta siempre en la primera
    random.shuffle(opciones)

    #  timer
    tiempo_total = 15
    ahora = datetime.utcnow().timestamp()
    start_time = session.get("pregunta_start_time")

    if not start_time:
        # primera vez que se muestra esta pregunta
        session["pregunta_start_time"] = ahora
        tiempo_restante = tiempo_total
    else:
        # calcular tiempo real restante
        transcurrido = ahora - start_time
        tiempo_restante = max(0, tiempo_total - transcurrido)

    # si se termina el tiempo, pasa a la siguiente pregunta
    if tiempo_restante <= 0:
        session["pregunta_start_time"] = None
        session["indice_actual"] = indice + 1
        return redirect(url_for("trivia_bp.trivia"))


    return render_template(
        "trivia.html",
        pregunta=pregunta,
        opciones=opciones,
        numero=indice + 1,
        total=len(preguntas_ids),
        tiempo_total=tiempo_restante
    )


# --- recibir respuesta ---
@trivia_bp.route("/responder", methods=["POST"])
def responder():
    opcion_id = int(request.form.get("opcion_id", 0))
    tiempo_total = float(request.form.get("tiempo_total", 15))
    tiempo_restante = float(request.form.get("tiempo_restante", tiempo_total))

    indice = session.get("indice_actual", 0)
    preguntas_ids = session.get("preguntas_ids", [])

    # si se alcanzo el limite de preguntas, termina la partida

    if indice >= len(preguntas_ids):
        return redirect(url_for("trivia_bp.fin_partida"))

    pregunta_id = preguntas_ids[indice]
    opcion = OpcionRespuesta.query.get(opcion_id)

    # puntaje base por dificultad
    dificultad_id = session.get("dificultad_id", 1)
    puntaje_base = {3: 5, 2: 10, 1: 15}.get(dificultad_id, 5)  # fácil=5, medio=10, difícil=15

    # puntaje bonus por tiempo restante (ej: 1 punto extra por cada segundo restante)
    bonus = max(0, int(tiempo_restante))
    puntos = 0
    es_correcta = False
    if opcion and opcion.es_correcta:
        puntos = puntaje_base + bonus
        es_correcta = True

    # actualizar puntaje en session
    session["score"] = session.get("score", 0) + puntos



    # pasar a siguiente pregunta al contestar
    session["indice_actual"] = indice + 1
    session["pregunta_start_time"] = None
    return redirect(url_for("trivia_bp.trivia"))


# fin de partida 
@trivia_bp.route("/fin", methods=["GET", "POST"])
def fin_partida():
    score = session.get("score", 0)
    preguntas_ids = session.get("preguntas_ids", [])

    if request.method == "POST":
        alias = request.form.get("alias", "Anónimo")
        jugador = Jugador.query.filter_by(alias=alias).first()
        if not jugador:
            jugador = Jugador(alias=alias)
            db.session.add(jugador)
            db.session.commit()

        # guarda la partida
        partida = Partida(
            jugador_id=jugador.jugador_id,
            fecha_inicio=datetime.utcnow(),
            fecha_fin=datetime.utcnow(),
            dificultad_id=session.get("dificultad_id"),
            puntaje_total=score,
            num_preguntas=len(preguntas_ids),
        )
        db.session.add(partida)
        db.session.commit()

        # borra la sesión para empezar otro juego (te vuelve a mandar a la pagina de configuracion)
        session.pop("preguntas_ids", None)
        session.pop("indice_actual", None)
        session.pop("score", None)
        session.pop("dificultad_id", None)
        session.pop("categoria_ids", None)
        session.pop("start_time", None)

        return redirect(url_for("trivia_bp.empezar"))

    return render_template("fin_partida.html", score=score)
