from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración básica de la base de datos
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    raise ValueError("DATABASE_URL no está configurada en el entorno.")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Rutas básicas para probar
@app.route('/')
def home():
    return "¡Conexión exitosa a la base de datos!"

if __name__ == '__main__':
    app.run(debug=True)
