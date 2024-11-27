from flask import Flask, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
from utils.pdf_generator import generar_pdf_proforma, generar_pdf_orden
from models import db, Cliente, Vehiculo, Proforma, OrdenServicio
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([cliente.to_dict() for cliente in clientes])

@app.route('/proformas/<int:proforma_id>/pdf', methods=['GET'])
def generar_proforma_pdf(proforma_id):
    try:
        file_path = generar_pdf_proforma(proforma_id)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": "Error al generar el PDF", "detalle": str(e)}), 500

@app.route('/ordenes/<int:orden_id>/pdf', methods=['GET'])
def generar_orden_pdf(orden_id):
    try:
        file_path = generar_pdf_orden(orden_id)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": "Error al generar el PDF", "detalle": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
