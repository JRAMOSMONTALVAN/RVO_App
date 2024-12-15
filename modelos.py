from extensions import db

class Cliente(db.Model):
    __tablename__ = "cliente"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120))
    documento = db.Column(db.String(20))
    telefono = db.Column(db.String(15))
    email = db.Column(db.String(120))


class Vehiculo(db.Model):
    __tablename__ = "vehiculo"
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    placa = db.Column(db.String(10))
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(50))
    año = db.Column(db.Integer)


class Proforma(db.Model):
    __tablename__ = "proforma"
    id = db.Column(db.Integer, primary_key=True)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculo.id'))
    total = db.Column(db.Float)
    detalles = db.Column(db.String(255))


class OrdenServicio(db.Model):
    __tablename__ = "orden_servicio"
    id = db.Column(db.Integer, primary_key=True)
    proforma_id = db.Column(db.Integer, db.ForeignKey('proforma.id'))
    estado = db.Column(db.String(50))
    observaciones = db.Column(db.String(255))
