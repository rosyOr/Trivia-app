from app.extensions import db

class Dificultad(db.Model):
    __tablename__ = "dificultad"

    dificultad_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre        = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<Dificultad {self.nombre}>"
