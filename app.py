# app/__init__.py
from flask import Flask
from app.extensions import db

def create_app():
    app = Flask(__name__)
    db.init_app(app)


    from app.cli import register_cli
    register_cli(app)

    return app
