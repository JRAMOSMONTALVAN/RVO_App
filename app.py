import os
from flask import Flask

# Configuración de la aplicación Flask
taller_app = Flask(__name__)

# Configuración de la SECRET_KEY desde las variables de entorno
# Si no está configurada en Railway, usa una clave predeterminada solo para pruebas locales.
taller_app.secret_key = os.getenv('SECRET_KEY', 'clave_por_defecto_123456')

# Ruta de prueba
@taller_app.route('/')
def home():
    return "¡Bienvenido a la aplicación del Taller Mecánico!"

# Exponemos `taller_app` como `app` para que Gunicorn lo use
app = taller_app
