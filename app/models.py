from .extensions import db
from datetime import datetime

# Definición básica del modelo de usuario
class User(db.Model):
    __tablename__ = 'user' # Nombre de la tabla en MySQL

    # Campos mínimos para que la aplicación no falle al iniciar
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    # Campo extra que es común
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

