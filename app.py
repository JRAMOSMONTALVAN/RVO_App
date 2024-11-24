from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configurar la aplicación Flask
taller_app = Flask(__name__)
taller_app.secret_key = os.urandom(24)  # Clave secreta para usar mensajes flash

# Configuración de la base de datos PostgreSQL
db_url = os.getenv('DATABASE_URL')
if db_url is None:
    raise ValueError("DATABASE_URL no está configurada. Asegúrate de tener un archivo .env con la conexión a la base de datos.")
taller_app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://", 1)
taller_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crear una instancia de SQLAlchemy
db = SQLAlchemy(taller_app)

# Modelo para Clientes
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_apellidos = db.Column(db.String(150), nullable=False)
    documento = db.Column(db.String(50), nullable=False, unique=True)
    telefono = db.Column(db.String(9), nullable=False)
    email = db.Column(db.String(100))
    vehiculos = db.relationship('Vehiculo', backref='cliente', lazy=True)

# Modelo para Vehículos
class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    placa = db.Column(db.String(6), nullable=False, unique=True)
    modelo = db.Column(db.String(100), nullable=False)
    ano_vehiculo = db.Column(db.String(4), nullable=False)

# Modelo para Proformas
class Proforma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    igv = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    items = db.relationship('ProformaItem', backref='proforma', lazy=True)

# Modelo para Items de Proforma
class ProformaItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proforma_id = db.Column(db.Integer, db.ForeignKey('proforma.id'), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

# Ruta principal
@taller_app.route('/')
def home():
    return render_template('index.html')

# Ruta para listar vehículos
@taller_app.route('/vehiculos', methods=['GET'])
def vehiculos():
    return render_template('vehiculos.html')

# Ruta para verificar un cliente
@taller_app.route('/verificar_cliente', methods=['POST'])
def verificar_cliente():
    documento = request.form.get('documento')  # Obtener el documento del formulario
    cliente = Cliente.query.filter_by(documento=documento).first()  # Buscar cliente en la base de datos

    if cliente:
        flash(f'Cliente encontrado: {cliente.nombre_apellidos}', 'success')
        return redirect(url_for('home'))
    else:
        flash('No se encontró un cliente con el documento proporcionado.', 'error')
        return redirect(url_for('home'))

# Ruta para registrar un vehículo
@taller_app.route('/registrar_vehiculo', methods=['POST'])
def registrar_vehiculo():
    # Aquí se manejaría la lógica para registrar un vehículo
    return "Vehículo registrado"

# Ejecutar la aplicación
if __name__ == '__main__':
    with taller_app.app_context():
        db.create_all()  # Crear las tablas si no existen
    taller_app.run(debug=True)
