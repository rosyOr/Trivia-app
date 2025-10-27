from app.extensions import db
from datetime import datetime

class Respuesta(db.Model):
    __tablename__ = 'respuesta'
    respuesta_id = db.Column(db.BigInteger, primary_key=True)
    partida_id = db.Column(db.BigInteger, db.ForeignKey('partida.partida_id'), nullable=False)
    pregunta_id = db.Column(db.BigInteger, db.ForeignKey('pregunta.pregunta_id'), nullable=False)
    opcion_id = db.Column(db.BigInteger, db.ForeignKey('opcion_respuesta.opcion_id'), nullable=False)
    es_correcta = db.Column(db.Boolean, nullable=False)
    puntos_otorgados = db.Column(db.Integer, default=0)
    respondida_en = db.Column(db.DateTime, default=datetime.utcnow)
