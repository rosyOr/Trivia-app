# app/cli.py
import click
from flask.cli import with_appcontext


from app.services.ingesta_service import importar_desde_opentdb
from app.services.seeds_service import seed_basico

@click.command(name="seed")                
@with_appcontext
def seed_command():
    """Carga datos iniciales (catálogos)."""
    seed_basico()
    click.echo("Seed ok")

@click.command(name="import-opentdb")      
@click.option("--amount", "-n", type=int, default=50)
@click.option("--category-id", type=int, default=None)
@click.option("--difficulty", type=click.Choice(["easy", "medium", "hard"]), default=None)
@click.option("--qtype", type=click.Choice(["multiple", "boolean"]), default="multiple")
@click.option("--use-token/--no-token", default=False)
@with_appcontext
def import_opentdb_cmd(amount, category_id, difficulty, qtype, use_token):
    """Importa preguntas desde OpenTriviaDB a la BD local."""
    importar_desde_opentdb(amount, category_id, difficulty, qtype, use_token)
    click.echo(f"Importación completada (solicitadas {amount}).")
