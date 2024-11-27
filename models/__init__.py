from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    documento = db.Column(db.String(20))
    telefono = db.Column(db.String(15))
    email = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "documento": self.documento,
            "telefono": self.telefono,
            "email": self.email
        }

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    placa = db.Column(db.String(10), unique=True)
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(50))
    anio = db.Column(db.Integer)
    kilometraje = db.Column(db.Integer)

class Proforma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), nullable=False)
    total = db.Column(db.Float)
    detalles = db.Column(db.Text)

class OrdenServicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proforma_id = db.Column(db.Integer, db.ForeignKey('proforma.id'), nullable=False)
    estado = db.Column(db.String(50))
    observaciones = db.Column(db.Text)
