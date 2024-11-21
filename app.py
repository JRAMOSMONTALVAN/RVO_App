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
    documento = db.Column(db.String(50), nullable=False)
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
    descripcion_servicio = db.Column(db.String(200), nullable=False)
    kilometraje = db.Column(db.String(20), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    igv = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    cliente = db.relationship('Cliente', backref=db.backref('proformas', lazy=True))
    vehiculo = db.relationship('Vehiculo', backref=db.backref('proformas', lazy=True))

# Ruta principal para mostrar los formularios de cliente y vehículo
@taller_app.route('/')
def home():
    clientes = Cliente.query.all()
    return render_template('index.html', clientes=clientes)

# Ruta para procesar el formulario de ingreso de cliente
@taller_app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    nombre_apellidos = request.form.get('nombre_apellidos')
    documento = request.form.get('documento')
    telefono = request.form.get('telefono')
    email = request.form.get('email')

    # Verificar que todos los campos obligatorios estén completos
    if not nombre_apellidos or not documento or not telefono:
        flash('Por favor, completa todos los campos obligatorios', 'danger')
        return redirect(url_for('home'))

    # Crear una nueva entrada en la base de datos
    nuevo_cliente = Cliente(
        nombre_apellidos=nombre_apellidos,
        documento=documento,
        telefono=telefono,
        email=email
    )

    # Agregar y confirmar los cambios en la base de datos
    try:
        db.session.add(nuevo_cliente)
        db.session.commit()
        # Agregar un mensaje de confirmación
        flash('Cliente agregado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al agregar el cliente: ' + str(e), 'danger')

    return redirect(url_for('home'))

# Ruta para procesar el formulario de ingreso de vehículo
@taller_app.route('/agregar_vehiculo', methods=['POST'])
def agregar_vehiculo():
    cliente_id = request.form['cliente_id']
    placa = request.form['placa']
    modelo = request.form['modelo']
    ano_vehiculo = request.form['ano_vehiculo']

    # Crear una nueva entrada en la base de datos
    nuevo_vehiculo = Vehiculo(
        cliente_id=cliente_id,
        placa=placa,
        modelo=modelo,
        ano_vehiculo=ano_vehiculo
    )
    
    # Agregar y confirmar los cambios en la base de datos
    db.session.add(nuevo_vehiculo)
    db.session.commit()

    return redirect(url_for('home'))

# Ruta para listar los clientes ingresados
@taller_app.route('/clientes')
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

# Ruta para mostrar el formulario de proforma
@taller_app.route('/proforma')
def proforma():
    clientes = Cliente.query.all()
    vehiculos = Vehiculo.query.all()
    return render_template('proforma.html', clientes=clientes, vehiculos=vehiculos)

# Ruta para procesar el formulario de proforma
@taller_app.route('/agregar_proforma', methods=['POST'])
def agregar_proforma():
    cliente_id = request.form['cliente_id']
    vehiculo_id = request.form['vehiculo_id']
    descripcion_servicio = request.form['descripcion_servicio']
    kilometraje = request.form['kilometraje']
    cantidad = int(request.form['cantidad'])
    precio_unitario = float(request.form['precio_unitario'])
    subtotal = cantidad * precio_unitario
    igv = subtotal * 0.18
    total = subtotal + igv

    # Crear una nueva entrada en la base de datos
    nueva_proforma = Proforma(
        cliente_id=cliente_id,
        vehiculo_id=vehiculo_id,
        descripcion_servicio=descripcion_servicio,
        kilometraje=kilometraje,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        subtotal=subtotal,
        igv=igv,
        total=total
    )
    
    # Agregar y confirmar los cambios en la base de datos
    db.session.add(nueva_proforma)
    db.session.commit()

    return redirect(url_for('proforma'))

# Inicializar la base de datos si no existe
with taller_app.app_context():
    db.create_all()

def open_browser():
    time.sleep(2)  # Espera breve para asegurar que el servidor esté listo
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    port = int(os.environ.get('PORT', 5000))
    taller_app.run(host='0.0.0.0', port=port, debug=False)
