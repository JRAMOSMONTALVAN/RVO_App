from models import db

class Proforma(db.Model):
    __tablename__ = 'proforma'

    id = db.Column(db.Integer, primary_key=True)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    detalles = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'vehiculo_id': self.vehiculo_id,
            'total': self.total,
            'detalles': self.detalles
        }
