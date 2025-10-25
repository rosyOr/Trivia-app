from app.extensions import db
from datetime import datetime


class Jugador(db.Model):
    __tablename__ = 'jugador'
    jugador_id = db.Column(db.BigInteger, primary_key=True)
    alias = db.Column(db.String(50), unique=True, nullable=False)
    fecha_alta = db.Column(db.DateTime, default=datetime.utcnow)