from app.extensions import db

class Pregunta(db.Model):
    __tablename__ = "pregunta"

    pregunta_id      = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    # Texto que mostrará el juego (ES). Por ahora, si aún no traduces, guardamos el EN aquí también.
    enunciado        = db.Column(db.Text, nullable=False)

    # Texto fuente original en inglés (para hashing/idempotencia de ingesta)
    enunciado_src_en = db.Column(db.Text, nullable=True)

    # Columna generada por MySQL (STORED): SHA2(enunciado_src_en, 256) → 64 hex chars
    enunciado_hash_en = db.Column(
        db.String(64),
        db.Computed("SHA2(enunciado_src_en, 256)", persisted=True),
        unique=True,
        nullable=True
    )

    categoria_id  = db.Column(db.Integer, db.ForeignKey("categoria.categoria_id"), nullable=False)
    dificultad_id = db.Column(db.Integer, db.ForeignKey("dificultad.dificultad_id"), nullable=False)
    imagen_id     = db.Column(db.BigInteger, db.ForeignKey("imagen.imagen_id"), nullable=True)

    categoria  = db.relationship("Categoria", backref="preguntas")
    dificultad = db.relationship("Dificultad", backref="preguntas")
    imagen     = db.relationship("Imagen", backref="preguntas")

    # hijos
    opciones = db.relationship(
        "OpcionRespuesta",
        back_populates="pregunta",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="OpcionRespuesta.opcion_id",
    )

    def __repr__(self):
        return f"<Pregunta {self.pregunta_id}>"
