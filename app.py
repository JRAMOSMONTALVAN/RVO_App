from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os

# Configurar la aplicación Flask
taller_app = Flask(__name__)
taller_app.secret_key = os.urandom(24)  # Necesario para usar flash messages

# Configuración de la base de datos PostgreSQL desde Heroku
taller_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
taller_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crear una instancia de la base de datos
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

# Ruta para agregar proformas
@taller_app.route('/agregar_proforma', methods=['POST'])
def agregar_proforma():
    cliente_id = request.form.get('cliente_id')
    vehiculo_id = request.form.get('vehiculo_id')
    fecha = date.today()
    items = [
        {"descripcion": request.form.get('descripcion1'), "cantidad": int(request.form.get('cantidad1')), "precio_unitario": float(request.form.get('precio_unitario1'))},
        {"descripcion": request.form.get('descripcion2'), "cantidad": int(request.form.get('cantidad2')), "precio_unitario": float(request.form.get('precio_unitario2'))}
    ]

    subtotal = sum(item["cantidad"] * item["precio_unitario"] for item in items)
    igv = round(subtotal * 0.18, 2)
    total = round(subtotal + igv, 2)

    nueva_proforma = Proforma(
        cliente_id=cliente_id,
        vehiculo_id=vehiculo_id,
        fecha=fecha,
        subtotal=subtotal,
        igv=igv,
        total=total
    )
    db.session.add(nueva_proforma)
    db.session.commit()

    for item in items:
        nuevo_item = ProformaItem(
            proforma_id=nueva_proforma.id,
            descripcion=item["descripcion"],
            cantidad=item["cantidad"],
            precio_unitario=item["precio_unitario"],
            total=item["cantidad"] * item["precio_unitario"]
        )
        db.session.add(nuevo_item)

    db.session.commit()
    flash('Proforma creada exitosamente', 'success')
    return redirect(url_for('home'))

# Inicializar la base de datos en Heroku
with taller_app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    taller_app.run(host='0.0.0.0', port=port, debug=True)
