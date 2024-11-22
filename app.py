from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
import webbrowser
import threading
import time

# Configurar la aplicación Flask
taller_app = Flask(__name__)
taller_app.secret_key = os.urandom(24)  # Necesario para usar flash messages

# Configuración de la base de datos SQLite
taller_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taller_mecanico.db'
# Desactiva el seguimiento de modificaciones para mejorar el rendimiento, ya que consume recursos adicionales.
taller_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crear una instancia de la base de datos
db = SQLAlchemy(taller_app)

# Modelo para Clientes
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_apellidos = db.Column(db.String(150), nullable=False)
    documento = db.Column(db.String(50), nullable=False, unique=True)  # Añadido unique=True para evitar duplicados
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

# Ruta principal para mostrar el formulario de ingreso del documento
@taller_app.route('/')
def home():
    documento = request.args.get('documento', '')
    cliente = None
    editar = False
    if documento and documento != 'None':
        cliente = Cliente.query.filter_by(documento=documento).first()
        if cliente:
            editar = True
    return render_template('index.html', documento=documento, cliente=cliente, editar=editar)

# Ruta para verificar si el cliente ya existe
@taller_app.route('/verificar_cliente', methods=['POST'])
def verificar_cliente():
    documento = request.form.get('documento')

    # Verificar si el documento tiene una longitud válida (DNI: 8 dígitos, RUC: 11 dígitos)
    if len(documento) not in [8, 11] or not documento.isdigit():
        flash('El documento debe tener 8 dígitos (DNI) o 11 dígitos (RUC).', 'danger')
        return redirect(url_for('home', documento=documento))

    # Verificar si ya existe un cliente con el mismo documento
    cliente = Cliente.query.filter_by(documento=documento).first()
    if cliente:
        # Si el cliente existe, mostrar los datos para editar
        flash('Cliente encontrado. Puedes editar la información.', 'info')
        return redirect(url_for('home', documento=documento))
    else:
        # Si el cliente no existe, permitir el registro
        flash('Cliente no encontrado. Ingresa la información para registrarlo.', 'warning')
        return redirect(url_for('home', documento=documento))

# Ruta para procesar el formulario de ingreso o edición de cliente
@taller_app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    nombre_apellidos = request.form.get('nombre_apellidos')
    documento = request.form.get('documento')
    telefono = request.form.get('telefono')
    email = request.form.get('email')

    # Verificar que todos los campos obligatorios estén completos
    if not nombre_apellidos or not documento or not telefono:
        flash('Por favor, completa todos los campos obligatorios', 'danger')
        return render_template('index.html', documento=documento, nombre_apellidos=nombre_apellidos, telefono=telefono, email=email, editar=False)

    # Verificar si ya existe un cliente con el mismo documento
    cliente_existente = Cliente.query.filter_by(documento=documento).first()
    if cliente_existente:
        # Si el cliente ya existe, actualizar la información
        cliente_existente.nombre_apellidos = nombre_apellidos
        cliente_existente.telefono = telefono
        cliente_existente.email = email
        db.session.commit()
        flash('Información del cliente actualizada exitosamente.', 'success')
    else:
        # Crear una nueva entrada en la base de datos
        nuevo_cliente = Cliente(
            nombre_apellidos=nombre_apellidos,
            documento=documento,
            telefono=telefono,
            email=email
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
        flash('Cliente agregado exitosamente.', 'success')

    # Limpiar el formulario después de agregar cliente exitosamente
    return redirect(url_for('home'))

# Ruta para ver la lista de clientes
@taller_app.route('/clientes')
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

# Inicializar la base de datos si no existe
with taller_app.app_context():
    db.create_all()

def open_browser():
    time.sleep(2)  # Espera breve para asegurar que el servidor esté listo
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    port = int(os.environ.get('PORT', 5000))
    taller_app.run(host='0.0.0.0', port=port, debug=True)
