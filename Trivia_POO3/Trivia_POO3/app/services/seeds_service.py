from app.extensions import db
from app.models.categoria import Categoria

CATS = ["Cultura General", "Geografía", "Historia", "Ciencia", "Deportes"]

def seed_basico():
    for nombre in CATS:
        if not Categoria.query.filter_by(nombre=nombre).first():
            db.session.add(Categoria(nombre=nombre))
    db.session.commit()
