from app import create_app
from app.cli import import_opentdb_cmd
app = create_app()

if __name__ == "__main__":
    app.run()

app.cli.add_command(import_opentdb_cmd)
