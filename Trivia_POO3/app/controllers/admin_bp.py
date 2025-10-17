from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.categoria import Categoria

admin_bp = Blueprint("admin", __name__)

@admin_bp.get("/categorias")
def listar_categorias():
    data = [{"id": c.categoria_id, "nombre": c.nombre} for c in Categoria.query.all()]
    return jsonify(data)

@admin_bp.post("/categorias")
def crear_categoria():
    nombre = (request.json or {}).get("nombre")
    if not nombre:
        return {"error": "nombre requerido"}, 400
    c = Categoria(nombre=nombre)
    db.session.add(c)
    db.session.commit()
    return {"id": c.categoria_id, "nombre": c.nombre}, 201
