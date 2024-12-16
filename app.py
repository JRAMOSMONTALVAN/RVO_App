from flask import Flask, jsonify

app = Flask(__name__)

# Ruta principal
@app.route("/")
def home():
    return jsonify({"mensaje": "Bienvenido a la API del Taller Mecánico"})

# Ruta para clientes
@app.route("/clientes", methods=["GET"])
def obtener_clientes():
    clientes = [
        {"id": 1, "nombre": "Juan Pérez"},
        {"id": 2, "nombre": "Ana Gómez"}
    ]
    return jsonify(clientes)

# Ruta para vehículos
@app.route("/vehiculos", methods=["GET"])
def obtener_vehiculos():
    vehiculos = [
        {"id": 1, "marca": "Toyota", "modelo": "Corolla", "placa": "XYZ-123"},
        {"id": 2, "marca": "Nissan", "modelo": "Sentra", "placa": "ABC-456"}
    ]
    return jsonify(vehiculos)

# Ruta para proformas
@app.route("/proformas", methods=["GET"])
def obtener_proformas():
    proformas = [
        {"id": 1, "descripcion": "Cambio de aceite", "costo": 100.0},
        {"id": 2, "descripcion": "Revisión de frenos", "costo": 150.0}
    ]
    return jsonify(proformas)

# Punto de entrada
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
