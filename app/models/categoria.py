from app.extensions import db

class Categoria(db.Model):
    __tablename__ = "categoria"
    categoria_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Categoria {self.nombre}>"

