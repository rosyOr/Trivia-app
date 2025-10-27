from app.extensions import db
from datetime import datetime



class PartidaPregunta(db.Model):
    __tablename__ = 'partida_pregunta'
    partida_id = db.Column(db.BigInteger, db.ForeignKey('partida.partida_id'), primary_key=True)
    pregunta_id = db.Column(db.BigInteger, db.ForeignKey('pregunta.pregunta_id'), primary_key=True)
    nro_orden = db.Column(db.Integer, nullable=False)