from app.extensions import db

class OpcionRespuesta(db.Model):
    __tablename__ = "opcion_respuesta"
    __table_args__ = (
        # evita duplicar el mismo texto de opción para la misma pregunta
        db.UniqueConstraint("pregunta_id", "texto", name="uq_opcion_texto"),
    )

    opcion_id   = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    pregunta_id = db.Column(db.BigInteger, db.ForeignKey("pregunta.pregunta_id"), nullable=False)
    texto       = db.Column(db.String(500), nullable=False)
    es_correcta = db.Column(db.Boolean, nullable=False, default=False)

    # Relación inversa
    pregunta = db.relationship("Pregunta", back_populates="opciones")

    def __repr__(self):
        return f"<Opcion {self.opcion_id} correcta={self.es_correcta}>"

