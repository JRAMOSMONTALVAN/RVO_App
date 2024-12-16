from flask import Flask, jsonify
from extensions import db, migrate
from modelos import Cliente, Vehiculo, Proforma, OrdenServicio

def create_app():
    # Inicializamos la aplicación Flask
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taller_mecanico.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializamos las extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Ruta principal
    @app.route("/")
    def home():
        return jsonify({"mensaje": "Bienvenido a la API del Taller Mecánico"})

    # Ruta para obtener clientes
    @app.route("/clientes", methods=["GET"])
    def obtener_clientes():
        clientes = [
            {"id": 1, "nombre": "Juan Pérez", "documento": "12345678"},
            {"id": 2, "nombre": "Ana Gómez", "documento": "87654321"},
        ]
        return jsonify(clientes)

    # Ruta para obtener vehículos
    @app.route("/vehiculos", methods=["GET"])
    def obtener_vehiculos():
        vehiculos = [
            {"id": 1, "placa": "ABC-123", "marca": "Toyota", "modelo": "Corolla"},
            {"id": 2, "placa": "XYZ-789", "marca": "Nissan", "modelo": "Versa"},
        ]
        return jsonify(vehiculos)

    # Ruta para obtener proformas
    @app.route("/proformas", methods=["GET"])
    def obtener_proformas():
        proformas = [
            {"id": 1, "descripcion": "Cambio de aceite", "costo": 100.0},
            {"id": 2, "descripcion": "Revisión general", "costo": 150.0},
        ]
        return jsonify(proformas)

    return app

# Creamos la instancia de la aplicación
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
