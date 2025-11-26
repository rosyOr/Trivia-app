from flask import Flask
from .extensions import db, migrate, init_cors
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    init_cors(app)

    # Blueprints
    from .controllers.admin_bp import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    from .cli import seed_command
    from .cli import import_opentdb_cmd
    app.cli.add_command(seed_command)
    app.cli.add_command(import_opentdb_cmd)

    from .controllers.trivia_bp import trivia_bp
    app.register_blueprint(trivia_bp, url_prefix="/trivia")
    

    return app
