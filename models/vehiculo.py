from models import db

class Vehiculo(db.Model):
    __tablename__ = 'vehiculo'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    placa = db.Column(db.String(10), unique=True, nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    kilometraje = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'placa': self.placa,
            'marca': self.marca,
            'modelo': self.modelo,
            'anio': self.anio,
            'kilometraje': self.kilometraje
        }
