# Script para organizar las subcategorias en una sola (ciencia y entretenimiento)

from app import create_app, db
from app.models.categoria import Categoria
from app.models.pregunta import Pregunta

def unificar_categoria(nombre_principal, patron_subcats):
    # Busca subcategorías
    subcats = Categoria.query.filter(Categoria.nombre.like(patron_subcats)).all()
    if not subcats:
        return

    # Busca la categoria main
    cat_main = Categoria.query.filter_by(nombre=nombre_principal).first()
    if not cat_main:
        cat_main = Categoria(nombre=nombre_principal)
        db.session.add(cat_main)
        db.session.flush()  # genera el ID sin hacer commit

    # Reasigna preguntas y elimina subcategorías
    for c in subcats:
        Pregunta.query.filter_by(categoria_id=c.categoria_id).update({
            "categoria_id": cat_main.categoria_id
        })
        db.session.delete(c)

    print(f"Subcategorías de '{nombre_principal}' unificadas en una sola.")

app = create_app()
with app.app_context():
    unificar_categoria("Entretenimiento", "Entretenimiento%")
    unificar_categoria("Ciencia", "Ciencia%")
    db.session.commit()