from app.extensions import db

class ProveedorApi(db.Model):
    __tablename__ = "proveedor_api"

    proveedor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre       = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<ProveedorApi {self.nombre}>"
