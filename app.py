@taller_app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    nombre_apellidos = request.form.get('nombre_apellidos')
    documento = request.form.get('documento')
    telefono = request.form.get('telefono')
    email = request.form.get('email')

    # Verificar que todos los campos obligatorios estén completos
    if not nombre_apellidos or not documento or not telefono:
        flash('Por favor completa todos los campos obligatorios', 'danger')
        return render_template('index.html', documento=documento, nombre_apellidos=nombre_apellidos, telefono=telefono, email=email, editar=False)

    # Verificar si ya existe un cliente con el mismo documento
    cliente_existente = Cliente.query.filter_by(documento=documento).first()
    if cliente_existente:
        # Si el cliente ya existe, actualizar la información
        cliente_existente.nombre_apellidos = nombre_apellidos
        cliente_existente.telefono = telefono
        cliente_existente.email = email
        db.session.commit()
        flash('Información del cliente actualizada exitosamente.', 'success')
    else:
        # Crear una nueva entrada en la base de datos
        nuevo_cliente = Cliente(
            nombre_apellidos=nombre_apellidos,
            documento=documento,
            telefono=telefono,
            email=email
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
        flash('Cliente agregado exitosamente.', 'success')

    # Limpiar el formulario después de agregar cliente exitosamente
    return redirect(url_for('home', documento=''))
