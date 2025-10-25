import time, html, requests, hashlib
from app.extensions import db
from app.models.categoria import Categoria
from app.models.dificultad import Dificultad
from app.models.pregunta import Pregunta
from app.models.opcion_respuesta import OpcionRespuesta

OPENTDB_BASE = "https://opentdb.com"
print(f"Usando OpenTDB API base: {OPENTDB_BASE}")
RATE_SLEEP_SEC = 5  # OpenTDB limita a 1 request / 5s (response_code 5)

def _get_session_token() -> str:
    r = requests.get(f"{OPENTDB_BASE}/api_token.php", params={"command": "request"})
    r.raise_for_status()
    data = r.json()
    return data["token"]  # token de sesión (vence por inactividad a las 6h)

def _upsert_categoria(nombre: str) -> int:
    c = Categoria.query.filter_by(nombre=nombre).first()
    if not c:
        c = Categoria(nombre=nombre)
        db.session.add(c)
        db.session.flush()
    return c.categoria_id

def _upsert_dificultad(nombre: str) -> int:
    d = Dificultad.query.filter_by(nombre=nombre).first()
    if not d:
        d = Dificultad(nombre=nombre)
        db.session.add(d)
        db.session.flush()
    return d.dificultad_id

def _decode_item(item: dict) -> dict:
    # OpenTDB devuelve por defecto HTML entities; las decodificamos.
    q = html.unescape(item["question"])
    corr = html.unescape(item["correct_answer"])
    incs = [html.unescape(x) for x in item.get("incorrect_answers", [])]
    return {**item, "question": q, "correct_answer": corr, "incorrect_answers": incs}


def _exists_pregunta_by_en_hash(src_en: str) -> bool:
    # Igual que MySQL: SHA2(...,256) → 64 hex en minúsculas
    h = hashlib.sha256(src_en.encode("utf-8")).hexdigest()
    return db.session.query(Pregunta.pregunta_id)\
        .filter(Pregunta.enunciado_hash_en == h).first() is not None

def importar_desde_opentdb(amount: int, category_id: int | None, difficulty: str | None,
                           qtype: str = "multiple", use_token: bool = False):
    token = _get_session_token() if use_token else None
    restantes = amount

    while restantes > 0:
        por_lote = min(50, restantes)
        params = {"amount": por_lote, "type": qtype}
        if token:       params["token"] = token
        if category_id: params["category"] = int(category_id)
        if difficulty:  params["difficulty"] = difficulty

        r = requests.get(f"{OPENTDB_BASE}/api.php", params=params, timeout=30)
        r.raise_for_status()
        payload = r.json()
        code = payload.get("response_code", 1)

        if code == 0:
            results = payload.get("results", [])
            if not results: break

            for raw in results:
                item = _decode_item(raw)

                # Evitar duplicados por HASH (de enunciado_src_en)
                src_en = item["question"]
                if _exists_pregunta_by_en_hash(src_en):
                    continue  # ya importada

                # Upsert cat/dif (en EN por ahora)
                cat = Categoria.query.filter_by(nombre=item["category"]).first() or Categoria(nombre=item["category"])
                dif = Dificultad.query.filter_by(nombre=item["difficulty"]).first() or Dificultad(nombre=item["difficulty"])
                db.session.add(cat); db.session.add(dif); db.session.flush()

                # Insertar pregunta:
                # - enunciado (ES) → por ahora guardo el mismo EN (lo actualizas cuando traduzcas)
                # - enunciado_src_en (EN) → fuente para el hash
                p = Pregunta(
                    enunciado=src_en,            # TEMP: aún no traducido
                    enunciado_src_en=src_en,     # fuente para el hash
                    categoria_id=cat.categoria_id,
                    dificultad_id=dif.dificultad_id,
                    imagen_id=None
                )
                db.session.add(p); db.session.flush()

                # Opciones
                if item["type"] == "boolean":
                    corr = item["correct_answer"]
                    for opt in ["True", "False"]:
                        db.session.add(OpcionRespuesta(
                            pregunta_id=p.pregunta_id,
                            texto=opt,
                            es_correcta=(opt == corr)
                        ))
                else:
                    db.session.add(OpcionRespuesta(
                        pregunta_id=p.pregunta_id,
                        texto=item["correct_answer"],
                        es_correcta=True
                    ))
                    for inc in item["incorrect_answers"]:
                        db.session.add(OpcionRespuesta(
                            pregunta_id=p.pregunta_id,
                            texto=inc,
                            es_correcta=False
                        ))

            db.session.commit()
            restantes -= len(results)
            if restantes > 0:
                time.sleep(RATE_SLEEP_SEC)
        elif code == 1:
            break
        elif code in (3, 4):
            token = _get_session_token() if use_token else None
            continue
        elif code == 5:
            time.sleep(RATE_SLEEP_SEC + 1)
            continue
        else:
            raise RuntimeError(f"OpenTDB response_code={code} params={params}")

