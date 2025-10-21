# ----------------------------------------------------------------------
# IMPORTACIÓN DE MODELOS
# Estos imports aseguran que Flask-SQLAlchemy conozca todas las clases
# para poder crear las tablas en la base de datos.
# ----------------------------------------------------------------------

from .models.categoria import Categoria
from .models.dificultad import Dificultad
from .models.imagen import Imagen
from .models.pregunta import Pregunta
from .models.opcion_respuesta import OpcionRespuesta
from .models.proveedor_api import ProveedorApi

