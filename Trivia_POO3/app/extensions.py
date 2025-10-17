from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
def init_cors(app):
    CORS(app, resources={r"/*": {"origins": "*"}})
