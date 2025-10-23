# app/cli.py
import click
from flask.cli import with_appcontext
from app.services.ingesta_service import importar_desde_opentdb
from app.services.seeds_service import seed_basico
from app.services.pregunta_localizacion import backfill_src_from_current, translate_pending

@click.command(name="seed")
@with_appcontext
def seed_command():
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
    importar_desde_opentdb(amount, category_id, difficulty, qtype, use_token)
    click.echo(f"Importación completada (solicitadas {amount}).")

@click.command("trivia-backfill-en")
@with_appcontext
def trivia_backfill_en():
    backfill_src_from_current(batch_size=200, dry_run=False)
    click.echo("Backfill EN -> enunciado_src_en OK")

@click.command("trivia-translate-es")
@with_appcontext
def trivia_translate_es():
    translate_pending(batch_size_chars=30000, batch_size_rows=200, dry_run=False, sleep_seconds=0.5)
    click.echo("Traducción ES OK")

def register_cli(app):
    # Pequeño print de diagnóstico
    print("[CLI] Registrando comandos…")
    app.cli.add_command(seed_command)
    app.cli.add_command(import_opentdb_cmd)
    app.cli.add_command(trivia_backfill_en)
    app.cli.add_command(trivia_translate_es)
