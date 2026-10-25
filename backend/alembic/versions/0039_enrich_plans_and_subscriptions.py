"""enrich plans and subscriptions with description and audit timestamps

Revision ID: 0039
Revises: 0038
Create Date: 2026-10-24 23:45:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "0039"
down_revision = "0038"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Agregar columnas a 'plans'
    op.add_column("plans", sa.Column("description", sa.Text(), nullable=True))
    op.add_column("plans", sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True))
    op.add_column("plans", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))

    # 2. Agregar columnas a 'subscriptions'
    op.add_column("subscriptions", sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True))
    op.add_column("subscriptions", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))

    # 3. Poblar descripciones en planes existentes
    op.execute(
        """
        UPDATE plans 
        SET description = 'Plan esencial para boutiques individuales. Incluye hasta 2 sucursales activas y gestión estándar de inventario y ventas POS.'
        WHERE code = 'basic' AND (description IS NULL OR description = '');
        """
    )
    op.execute(
        """
        UPDATE plans 
        SET description = 'Plan avanzado para marcas en expansión. Incluye hasta 10 sucursales activas, analítica predictiva y asistente de voz con Gemini IA.'
        WHERE code = 'pro' AND (description IS NULL OR description = '');
        """
    )


def downgrade() -> None:
    op.drop_column("subscriptions", "updated_at")
    op.drop_column("subscriptions", "created_at")
    op.drop_column("plans", "updated_at")
    op.drop_column("plans", "created_at")
    op.drop_column("plans", "description")
