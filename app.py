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

# Ruta principal para mostrar el formulario de ingreso del documento
@taller_app.route('/')
def home():
    return render_template('index.html')

# Ruta para gestionar vehículos
@taller_app.route('/vehiculos', methods=['GET', 'POST'])
def vehiculos():
    if request.method == 'POST':
        # Capturar datos del formulario
        cliente_id = request.form.get('cliente_id')
        placa = request.form.get('placa')
        modelo = request.form.get('modelo')
        ano_vehiculo = request.form.get('ano_vehiculo')

        # Validar datos
        if not cliente_id or not placa or not modelo or not ano_vehiculo:
            flash('Todos los campos son obligatorios.', 'error')
        else:
            nuevo_vehiculo = Vehiculo(
                cliente_id=cliente_id,
                placa=placa,
                modelo=modelo,
                ano_vehiculo=ano_vehiculo
            )
            try:
                db.session.add(nuevo_vehiculo)
                db.session.commit()
                flash('Vehículo registrado exitosamente.', 'success')
            except Exception as e:
                flash(f'Error al registrar vehículo: {e}', 'error')

    # Obtener todos los vehículos
    lista_vehiculos = Vehiculo.query.all()
    return render_template('vehiculos.html', vehiculos=lista_vehiculos)

# Inicializar la base de datos en Heroku
with taller_app.app_context():
    db.create_all()

# Ejecutar la aplicación
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    taller_app.run(host='0.0.0.0', port=port, debug=True)
