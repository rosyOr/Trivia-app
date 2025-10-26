# Importa la instancia de DB desde las extensiones 
from ..extensions import db 

class Usuario(db.Model):
    __tablename__ = 'usuario' # Nombre de la tabla en la DB

    # Define una columna básica (ejemplo: ID)
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(80), unique=True, nullable=False) 

    def __repr__(self):
        return f'<Usuario {self.id}>'