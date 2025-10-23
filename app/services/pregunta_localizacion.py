from time import sleep
from sqlalchemy import or_
from app.extensions import db
from app.models.pregunta import Pregunta
from app.services.traduccion_servicio import translate_with_deepl

def backfill_src_from_current(batch_size=200, dry_run=True):
    
    q = (Pregunta.query
         .filter(or_(Pregunta.enunciado_src_en == None, Pregunta.enunciado_src_en == ""))
         .filter(Pregunta.enunciado != None)
         .order_by(Pregunta.pregunta_id))
    total = q.count()
    print(f"[BACKFILL] Filas a copiar enunciado -> enunciado_src_en: {total}")

    offset = 0
    procesadas = 0
    while True:
        items = q.limit(batch_size).offset(offset).all()
        if not items:
            break
        for row in items:
            src = (row.enunciado or "").strip()
            if not src:
                continue
            if dry_run:
                print(f"[DRY] {row.pregunta_id}: copia EN actual a enunciado_src_en")
            else:
                row.enunciado_src_en = src
        if not dry_run:
            db.session.commit()
        procesadas += len(items)
        offset += batch_size
        print(f"[BACKFILL] Lote listo. {procesadas}/{total}")
    print("[BACKFILL] Hecho.")

def translate_pending(batch_size_chars=30000, batch_size_rows=200, dry_run=True, sleep_seconds=1.0):
    
    base_q = (Pregunta.query
              .filter(Pregunta.enunciado_src_en != None)
              .order_by(Pregunta.pregunta_id))

    def needs_translation(row: Pregunta) -> bool:
        src = (row.enunciado_src_en or "").strip()
        dst = (row.enunciado or "").strip() if row.enunciado is not None else ""
        if not src:
            return False
        # Traducir si destino está vacío o si destino == fuente (todavía en EN)
        return (not dst) or (dst == src)

    # Traemos en bloques de filas
    offset = 0
    procesadas = 0
    while True:
        items = base_q.limit(batch_size_rows).offset(offset).all()
        if not items:
            break

        # Filtramos las que realmente necesitan traducción
        candidates = [r for r in items if needs_translation(r)]
        if not candidates:
            offset += batch_size_rows
            continue

        # Respetar un presupuesto de caracteres por lote
        char_budget = batch_size_chars
        will_process = []
        for r in candidates:
            ln = len(r.enunciado_src_en or "")
            if ln <= char_budget:
                will_process.append(r)
                char_budget -= ln
            else:
                break

        print(f"[TRANSLATE] Lote con {len(will_process)} filas, ~{batch_size_chars-char_budget} chars")

        for row in will_process:
            src = (row.enunciado_src_en or "").strip()
            try:
                es = translate_with_deepl(src)
            except Exception as e:
                print(f"[ERROR] {row.pregunta_id}: {e}")
                continue

            if dry_run:
                print(f"[DRY] {row.pregunta_id}: '{src[:70]}...' -> '{es[:70]}...'")
            else:
                row.enunciado = es
                # pequeña pausa
                sleep(sleep_seconds)

        if not dry_run:
            db.session.commit()
            print("[TRANSLATE] Cambios guardados.")

        procesadas += len(will_process)
        offset += batch_size_rows

    print(f"[TRANSLATE] Hecho. Total filas procesadas: {procesadas}")
