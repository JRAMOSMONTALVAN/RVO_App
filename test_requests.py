import requests

# Crear cliente
cliente_data = {
    "nombre": "Juan Pérez",
    "documento": "98765432",
    "telefono": "987654321",
    "email": "juan.perez@example.com"
}
response = requests.post("http://127.0.0.1:5000/clientes", json=cliente_data)
print("Crear Cliente:", response.json())

# Listar clientes
response = requests.get("http://127.0.0.1:5000/clientes")
print("Listar Clientes:", response.json())

# Crear vehículo
vehiculo_data = {
    "cliente_id": 1,
    "placa": "ABC123",
    "modelo": "Toyota Corolla",
    "anio": 2020
}
response = requests.post("http://127.0.0.1:5000/vehiculos", json=vehiculo_data)
print("Crear Vehículo:", response.json())

# Listar vehículos
response = requests.get("http://127.0.0.1:5000/vehiculos")
print("Listar Vehículos:", response.json())

# Crear proforma
proforma_data = {
    "cliente_id": 1,
    "vehiculo_id": 1,
    "marca": "Toyota",
    "modelo": "Corolla",
    "kilometraje": 50000,
    "subtotal": 100.0,
    "igv": 18.0,
    "total": 118.0,
    "detalles": [
        {"descripcion": "Cambio de aceite", "cantidad": 1, "precio_unitario": 50},
        {"descripcion": "Filtro de aire", "cantidad": 1, "precio_unitario": 50}
    ]
}
response = requests.post("http://127.0.0.1:5000/proformas", json=proforma_data)
print("Crear Proforma:", response.json())

# Listar proformas
response = requests.get("http://127.0.0.1:5000/proformas")
print("Listar Proformas:", response.json())
