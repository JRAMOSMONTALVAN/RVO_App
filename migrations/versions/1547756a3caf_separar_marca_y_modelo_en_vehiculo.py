"""Separar marca y modelo en Vehiculo

Revision ID: 1547756a3caf
Revises: <anterior_revision_id>
Create Date: 2024-11-26 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# Revisiones
revision = '1547756a3caf'
down_revision = '8583442aaef6'  # Reemplazar con la revisión anterior
branch_labels = None
depends_on = None


def upgrade():
    # Agregar las columnas 'marca' y 'kilometraje' inicialmente como NULL
    op.add_column('vehiculo', sa.Column('marca', sa.String(length=50), nullable=True))
    op.add_column('vehiculo', sa.Column('kilometraje', sa.Integer(), nullable=True))
    
    # Actualizar las filas existentes con valores por defecto para evitar NULL
    op.execute("UPDATE vehiculo SET marca = 'Desconocida' WHERE marca IS NULL")
    op.execute("UPDATE vehiculo SET kilometraje = 0 WHERE kilometraje IS NULL")
    
    # Cambiar las columnas para que sean NOT NULL
    op.alter_column('vehiculo', 'marca', nullable=False)
    op.alter_column('vehiculo', 'kilometraje', nullable=False)


def downgrade():
    # Revertir los cambios eliminando las columnas agregadas
    op.drop_column('vehiculo', 'marca')
    op.drop_column('vehiculo', 'kilometraje')
