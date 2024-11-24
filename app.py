import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicialización de la app Flask
app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Variable de entorno
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar el rastreo de modificaciones (recomendado)

# Inicializa la base de datos con SQLAlchemy
db = SQLAlchemy(app)

# Modelo de ejemplo (modifica según tus necesidades)
class ExampleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<ExampleModel {self.name}>"

# Ruta principal para probar
@app.route('/')
def home():
    return "¡Aplicación conectada a PostgreSQL correctamente!"

# Ejecuta la aplicación
if __name__ == '__main__':
    app.run(debug=True)
