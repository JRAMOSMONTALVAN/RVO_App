import requests

# Crear una nueva proforma
proforma_data = {
    "cliente_id": 1,
    "vehiculo_id": 1,
    "descripcion": "Cambio de aceite y revisión general",
    "costo_estimado": 150.75,
    "kilometraje": 45000,
    "marca": "Toyota",
    "modelo": "Corolla"
}
response = requests.post("http://127.0.0.1:5000/proformas", json=proforma_data)
print("Crear Proforma:", response.json())

# Listar todas las proformas
response = requests.get("http://127.0.0.1:5000/proformas")
print("Listar Proformas:", response.json())
