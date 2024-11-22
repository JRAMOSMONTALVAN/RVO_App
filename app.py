from flask import Flask, render_template, request, redirect, url_for, flash

# Inicializa la aplicación Flask
app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Cambia esto por una clave segura

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para verificar cliente
@app.route('/verificar_cliente', methods=['POST'])
def verificar_cliente():
    documento = request.form.get('documento')
    if not documento:
        flash('Por favor completa todos los campos obligatorios')
        return redirect(url_for('index', documento=documento))
    
    # Aquí iría la lógica para verificar el cliente
    return render_template('agregar_cliente.html', documento=documento)

# Ruta para agregar cliente
@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    documento = request.form.get('documento')
    nombre = request.form.get('nombre')
    telefono = request.form.get('telefono')
    
    if not documento or not nombre or not telefono:
        flash('Por favor completa todos los campos obligatorios')
        return redirect(url_for('index', documento=documento))

    # Aquí iría la lógica para agregar el cliente a la base de datos
    flash('Cliente agregado exitosamente')
    return redirect(url_for('index'))

# Ruta para mostrar lista de clientes
@app.route('/clientes')
def lista_clientes():
    # Aquí iría la lógica para obtener la lista de clientes de la base de datos
    clientes = []
    return render_template('clientes.html', clientes=clientes)

# Inicia la aplicación
if __name__ == '__main__':
    app.run(debug=True)
