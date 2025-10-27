import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.cli import import_opentdb_cmd
from flask import Blueprint, render_template
from app.extensions import db



trivia_bp = Blueprint("trivia", __name__)

app = create_app()
app.register_blueprint(trivia_bp, url_prefix="/trivia")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/info")
def info():
    return render_template("información.html")





if __name__ == "__main__":
    app.run(debug=True)

app.cli.add_command(import_opentdb_cmd)


