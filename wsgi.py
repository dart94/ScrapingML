import sys
import os

# Añadir el directorio de tu proyecto a sys.path
project_home = '/home/dart94/my_flask_app'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Establecer la variable de entorno FLASK_APP para apuntar a tu aplicación
os.environ['FLASK_APP'] = 'my_flask_app/app.py'

# Importar tu aplicación Flask pero llamarla "application" para que funcione con WSGI
from app import app as application  # noqa
