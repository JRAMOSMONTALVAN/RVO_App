from flask import Flask, request, render_template, redirect, url_for

# Crear la aplicación Flask
taller_app = Flask(__name__)

# Ruta para agregar un cliente (POST)
@taller_app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    # Aquí deberías manejar los datos que vienen del formulario
    documento = request.form.get('documento')
    nombre = request.form.get('nombre')
    telefono = request.form.get('telefono')
    correo = request.form.get('correo')
    
    # Validación para asegurar que se han completado todos los campos
    if not documento or not nombre or not telefono:
        error = "Por favor, completa todos los campos obligatorios"
        return render_template('agregar_cliente.html', error=error, documento=documento, nombre=nombre, telefono=telefono, correo=correo)
    
    # Código para guardar el cliente en la base de datos (si aplica)

    return redirect(url_for('ver_lista_clientes'))

# Ruta para ver la lista de clientes (GET)
@taller_app.route('/ver_lista_clientes', methods=['GET'])
def ver_lista_clientes():
    # Aquí se retornará la lista de clientes (deberías obtener los datos de la base de datos)
    return render_template('lista_clientes.html')

if __name__ == '__main__':
    taller_app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
