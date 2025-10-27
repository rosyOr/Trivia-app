import click
from flask.cli import with_appcontext
from app.services.ingesta_service import importar_desde_opentdb
from app.services.seeds_service import seed_basico
from app.extensions import db # Asegúrate de que db esté importado

@click.command(name="seed")
@with_appcontext
def seed_command():
    """Carga datos iniciales (catálogos)."""
    seed_basico()
    click.echo("Seed ok")

@click.command(name="import-opentdb")
@click.option("--amount", "-n", type=int, default=300)
@click.option("--category-id", type=int, default=None)
@click.option("--difficulty", type=click.Choice(["easy", "medium", "hard"]), default=None)
@click.option("--qtype", type=click.Choice(["multiple", "boolean"]), default="multiple")
@click.option("--use-token/--no-token", default=False)
@with_appcontext
def import_opentdb_cmd(amount, category_id, difficulty, qtype, use_token):
    """Importa preguntas desde OpenTriviaDB a la BD local, limpiando datos anteriores."""
    
    # --- PASO DE LIMPIEZA AUTOMÁTICA ---
    try:
        click.echo("--- Limpiando tablas existentes... ---")
        
        # Eliminar datos en el orden correcto (hijo a padre)
        db.session.execute(db.text("DELETE FROM opcion_respuesta;"))
        db.session.execute(db.text("DELETE FROM pregunta;"))
        db.session.execute(db.text("DELETE FROM categoria;"))
        
        # Resetear los contadores de ID para evitar conflictos de claves
        db.session.execute(db.text("ALTER TABLE pregunta AUTO_INCREMENT = 1;"))
        db.session.execute(db.text("ALTER TABLE opcion_respuesta AUTO_INCREMENT = 1;"))
        db.session.execute(db.text("ALTER TABLE categoria AUTO_INCREMENT = 1;"))
        
        db.session.commit()
        click.echo("Limpieza completada.")
        
    except Exception as e:
        db.session.rollback()
        click.echo(f"Error al limpiar la base de datos: {e}")
        return # Detiene el proceso si la limpieza falla

    # --- PASO DE IMPORTACIÓN ---
    click.echo(f"--- Iniciando importación de {amount} preguntas de OpenTDB ---")
    
    try:
        importar_desde_opentdb(amount, category_id, difficulty, qtype, use_token)
        click.echo(f"Importación completada (solicitadas {amount}).")
    except Exception as e:
        db.session.rollback()
        click.echo(f"[ERROR FATAL] La importación falló: {e}")