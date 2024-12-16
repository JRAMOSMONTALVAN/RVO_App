from flask import Flask, jsonify

# Instancia de Flask
app = Flask(__name__)

# Ruta principal
@app.route("/")
def home():
    return jsonify({"mensaje": "Bienvenido a la API del Taller Mecánico"})

# Ruta para clientes
@app.route("/clientes", methods=["GET"])
def obtener_clientes():
    return jsonify([
        {"id": 1, "nombre": "Juan Pérez"},
        {"id": 2, "nombre": "Ana Gómez"}
    ])

# Ruta para vehículos
@app.route("/vehiculos", methods=["GET"])
def obtener_vehiculos():
    return jsonify([
        {"id": 1, "marca": "Toyota", "modelo": "Corolla", "placa": "XYZ-123"},
        {"id": 2, "marca": "Nissan", "modelo": "Sentra", "placa": "ABC-456"}
    ])

# Ruta para proformas
@app.route("/proformas", methods=["GET"])
def obtener_proformas():
    return jsonify([
        {"id": 1, "descripcion": "Cambio de aceite", "costo": 100.0},
        {"id": 2, "descripcion": "Revisión de frenos", "costo": 150.0}
    ])

# Configuración para producción
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
