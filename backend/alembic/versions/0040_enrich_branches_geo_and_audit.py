"""enrich branches with geo coordinates, contact details and audit timestamps

Revision ID: 0040
Revises: 0039
Create Date: 2026-10-25 01:30:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0040"
down_revision = "0039"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Agregar columnas a 'branches'
    op.add_column("branches", sa.Column("address", sa.String(length=255), server_default="", nullable=False))
    op.add_column("branches", sa.Column("phone", sa.String(length=50), server_default="", nullable=False))
    op.add_column("branches", sa.Column("opening_hours", sa.String(length=100), server_default="09:00 - 20:00", nullable=False))
    op.add_column("branches", sa.Column("latitude", sa.Numeric(precision=10, scale=7), server_default="-17.7833000", nullable=False))
    op.add_column("branches", sa.Column("longitude", sa.Numeric(precision=10, scale=7), server_default="-63.1821000", nullable=False))
    op.add_column("branches", sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True))
    op.add_column("branches", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True))

    # 2. Poblar datos realistas para sucursales sembradas
    op.execute(
        """
        UPDATE branches
        SET address = 'Av. Monseñor Rivero #340, Centro',
            phone = '+591 3 3345678',
            opening_hours = '09:00 - 21:00',
            latitude = -17.7765000,
            longitude = -63.1812000
        WHERE name = 'Boutique Elegance - Central'
        """
    )
    op.execute(
        """
        UPDATE branches
        SET address = 'Av. San Martín y Calle 5 Este, Equipetrol',
            phone = '+591 3 3456789',
            opening_hours = '10:00 - 22:00',
            latitude = -17.7689000,
            longitude = -63.1934000
        WHERE name = 'Boutique Elegance - Equipetrol'
        """
    )
    op.execute(
        """
        UPDATE branches
        SET address = 'Calle Sucre #250, Casco Viejo',
            phone = '+591 4 4256789',
            opening_hours = '09:00 - 20:00',
            latitude = -17.3935000,
            longitude = -66.1570000
        WHERE name = 'Moda Urbana - Casco Viejo'
        """
    )


def downgrade() -> None:
    op.drop_column("branches", "updated_at")
    op.drop_column("branches", "created_at")
    op.drop_column("branches", "longitude")
    op.drop_column("branches", "latitude")
    op.drop_column("branches", "opening_hours")
    op.drop_column("branches", "phone")
    op.drop_column("branches", "address")
