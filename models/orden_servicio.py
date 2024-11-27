from models import db

class OrdenServicio(db.Model):
    __tablename__ = 'orden_servicio'

    id = db.Column(db.Integer, primary_key=True)
    proforma_id = db.Column(db.Integer, db.ForeignKey('proforma.id'), nullable=False)
    estado = db.Column(db.String(20), default='Pendiente', nullable=False)
    observaciones = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'proforma_id': self.proforma_id,
            'estado': self.estado,
            'observaciones': self.observaciones
        }
