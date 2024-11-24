from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
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

# Ruta principal
@taller_app.route('/')
def home():
    return render_template('index.html', editar=False, documento="", nombre_apellidos="", telefono="", email="")

# Ruta para verificar un cliente
@taller_app.route('/verificar_cliente', methods=['POST'])
def verificar_cliente():
    documento = request.form.get('documento')
    cliente = Cliente.query.filter_by(documento=documento).first()

    if cliente:
        return render_template(
            'index.html',
            editar=True,
            documento=cliente.documento,
            cliente=cliente,
            nombre_apellidos=cliente.nombre_apellidos,
            telefono=cliente.telefono,
            email=cliente.email
        )
    else:
        flash('No se encontró un cliente con el documento proporcionado.', 'danger')
        return redirect(url_for('home'))

# Ruta para agregar o actualizar un cliente
@taller_app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    documento = request.form.get('documento')
    cliente = Cliente.query.filter_by(documento=documento).first()

    if cliente:
        # Actualizar cliente existente
        cliente.nombre_apellidos = request.form['nombre_apellidos']
        cliente.telefono = request.form['telefono']
        cliente.email = request.form['email']
        flash('Cliente actualizado con éxito.', 'success')
    else:
        # Agregar nuevo cliente
        nuevo_cliente = Cliente(
            documento=documento,
            nombre_apellidos=request.form['nombre_apellidos'],
            telefono=request.form['telefono'],
            email=request.form['email']
        )
        db.session.add(nuevo_cliente)
        flash('Cliente agregado con éxito.', 'success')

    db.session.commit()
    return redirect(url_for('home'))

# Ejecutar la aplicación
if __name__ == '__main__':
    with taller_app.app_context():
        db.create_all()  # Crear las tablas si no existen
    port = int(os.environ.get('PORT', 5000))
    taller_app.run(host='0.0.0.0', port=port, debug=True)
