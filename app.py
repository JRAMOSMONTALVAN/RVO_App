import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date

# Configuración de la aplicación Flask
taller_app = Flask(__name__)
taller_app.secret_key = os.urandom(24)  # Necesario para usar flash messages

# Configuración de la base de datos PostgreSQL
taller_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
taller_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos con SQLAlchemy
db = SQLAlchemy(taller_app)

# Modelo de ejemplo (puedes personalizar según tus necesidades)
class ExampleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<ExampleModel {self.name}>"

# Ruta principal para probar
@taller_app.route('/')
def home():
    return render_template('index.html')

# Inicializar la base de datos
with taller_app.app_context():
    db.create_all()

# Ejecutar la aplicación
if __name__ == '__main__':
    taller_app.run(debug=True)
