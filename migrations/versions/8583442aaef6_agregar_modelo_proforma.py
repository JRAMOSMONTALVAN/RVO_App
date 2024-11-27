"""Agregar modelo Proforma

Revision ID: 8583442aaef6
Revises: 7a5b852ef8c2
Create Date: 2024-11-25 22:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8583442aaef6'
down_revision = '7a5b852ef8c2'
branch_labels = None
depends_on = None


def upgrade():
    # Crear tabla proforma
    op.create_table(
        'proforma',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('cliente_id', sa.Integer(), sa.ForeignKey('cliente.id'), nullable=False),
        sa.Column('vehiculo_id', sa.Integer(), sa.ForeignKey('vehiculo.id'), nullable=False),
        sa.Column('descripcion', sa.String(length=255), nullable=False),
        sa.Column('costo_estimado', sa.Float(), nullable=False),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('kilometraje', sa.Integer(), nullable=True),
        sa.Column('marca', sa.String(length=50), nullable=True),
        sa.Column('modelo', sa.String(length=50), nullable=True),
    )

    # Alterar columna 'anio' en tabla 'vehiculo' para cambiar su tipo a INTEGER
    with op.batch_alter_table('vehiculo', schema=None) as batch_op:
        batch_op.alter_column(
            'anio',
            existing_type=sa.String(length=4),
            type_=sa.Integer(),
            postgresql_using="anio::integer"
        )


def downgrade():
    # Eliminar tabla proforma
    op.drop_table('proforma')

    # Revertir tipo de columna 'anio' en tabla 'vehiculo'
    with op.batch_alter_table('vehiculo', schema=None) as batch_op:
        batch_op.alter_column(
            'anio',
            existing_type=sa.Integer(),
            type_=sa.String(length=4),
            postgresql_using="anio::text"
        )
