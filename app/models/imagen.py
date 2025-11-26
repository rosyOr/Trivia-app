from app.extensions import db
from sqlalchemy import CheckConstraint

class Imagen(db.Model):
    __tablename__ = "imagen"
    __table_args__ = (
        CheckConstraint("alto IS NULL OR alto > 0", name="chk_imagen_alto_pos"),
    )

    imagen_id      = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    proveedor_id   = db.Column(db.Integer, db.ForeignKey("proveedor_api.proveedor_id"), nullable=False)
    alto           = db.Column(db.Integer, nullable=True)               # px; opcional
    alt_text       = db.Column(db.String(255), nullable=True)           # accesibilidad/descripcion
    fecha_descarga = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    proveedor = db.relationship("ProveedorApi", backref="imagenes")

    def __repr__(self):
        return f"<Imagen {self.imagen_id} prov={self.proveedor_id}>"
