from flask import Flask, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound
from utils.pdf_generator import generar_pdf_proforma, generar_pdf_orden
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos desde DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de la base de datos
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelos
class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(20), nullable=False, unique=True)
    telefono = db.Column(db.String(15))
    email = db.Column(db.String(100))

class Proforma(db.Model):
    __tablename__ = 'proforma'
    id = db.Column(db.Integer, primary_key=True)
    vehiculo_id = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    detalles = db.Column(db.Text)

class OrdenServicio(db.Model):
    __tablename__ = 'orden_servicio'
    id = db.Column(db.Integer, primary_key=True)
    proforma_id = db.Column(db.Integer, db.ForeignKey('proforma.id'), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='Pendiente')
    observaciones = db.Column(db.Text)

# Rutas principales
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "mensaje": "Bienvenido a la API de Taller Mecánico",
        "endpoints": {
            "clientes": "/clientes",
            "proforma_pdf": "/proformas/<proforma_id>/pdf",
            "orden_pdf": "/ordenes/<orden_id>/pdf"
        }
    })

@app.route('/clientes', methods=['GET'])
def obtener_clientes():
    clientes = Cliente.query.all()
    resultado = [
        {"id": c.id, "nombre": c.nombre, "documento": c.documento, "telefono": c.telefono, "email": c.email}
        for c in clientes
    ]
    return jsonify(resultado)

@app.route('/proformas/<int:proforma_id>/pdf', methods=['GET'])
def descargar_proforma_pdf(proforma_id):
    try:
        file_path = generar_pdf_proforma(proforma_id)
        return send_file(file_path, as_attachment=True)
    except NotFound:
        return jsonify({"error": "Proforma no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al generar PDF: {str(e)}"}), 500

@app.route('/ordenes/<int:orden_id>/pdf', methods=['GET'])
def descargar_orden_pdf(orden_id):
    try:
        file_path = generar_pdf_orden(orden_id)
        return send_file(file_path, as_attachment=True)
    except NotFound:
        return jsonify({"error": "Orden de servicio no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al generar PDF: {str(e)}"}), 500

if __name__ == '__main__':
    app.run()
