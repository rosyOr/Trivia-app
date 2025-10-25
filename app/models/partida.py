from app.extensions import db
from datetime import datetime

class Partida(db.Model):
    __tablename__ = 'partida'
    partida_id = db.Column(db.BigInteger, primary_key=True)
    jugador_id = db.Column(db.BigInteger, db.ForeignKey('jugador.jugador_id'), nullable=False)
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_fin = db.Column(db.DateTime)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.categoria_id'))
    dificultad_id = db.Column(db.Integer, db.ForeignKey('dificultad.dificultad_id'))
    num_preguntas = db.Column(db.Integer)
    puntaje_total = db.Column(db.Integer, default=0)
    jugador = db.relationship('Jugador', backref='partidas')
    categoria = db.relationship('Categoria')
    dificultad = db.relationship('Dificultad')