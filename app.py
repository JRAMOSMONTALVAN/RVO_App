import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date

# Configuración de la aplicación Flask
taller_app = Flask(__name__)
taller_app.secret_key = os.urandom(24)  # Necesario para usar flash messages

# Configuración de la base de datos PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

taller_app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
taller_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos con SQLAlchemy
db = SQLAlchemy(taller_app)

# Modelo de ejemplo para prueba
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    documento = db.Column(db.String(20), nullable=False, unique=True)
    telefono = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f"<Cliente {self.nombre}>"

# Ruta principal para probar
@taller_app.route('/')
def home():
    return render_template('index.html')

# Ruta para agregar un cliente
@taller_app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    nombre = request.form.get('nombre')
    documento = request.form.get('documento')
    telefono = request.form.get('telefono')
    email = request.form.get('email')

    if not nombre or not documento:
        flash('El nombre y el documento son obligatorios', 'danger')
        return redirect(url_for('home'))

    nuevo_cliente = Cliente(nombre=nombre, documento=documento, telefono=telefono, email=email)
    try:
        db.session.add(nuevo_cliente)
        db.session.commit()
        flash('Cliente agregado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al agregar el cliente. Es posible que el documento ya exista.', 'danger')

    return redirect(url_for('home'))

# Inicializar la base de datos
with taller_app.app_context():
    db.create_all()

# Ejecutar la aplicación
if __name__ == '__main__':
    taller_app.run(host='0.0.0.0', port=8080, debug=True)
