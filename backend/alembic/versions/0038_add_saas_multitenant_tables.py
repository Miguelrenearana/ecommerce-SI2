"""add saas multitenant tables (companies, plans, subscriptions) and tenant_id columns

Revision ID: 0038
Revises: 0037
Create Date: 2026-10-24 10:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0038"
down_revision = "0037"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Crear tabla 'companies'
    op.create_table(
        "companies",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("business_name", sa.String(length=200), nullable=False),
        sa.Column("nit_rut", sa.String(length=50), nullable=False),
        sa.Column("subdomain", sa.String(length=63), nullable=False),
        sa.Column("status", sa.String(length=20), server_default="ACTIVO", nullable=False),
        sa.Column("email", sa.String(length=120), nullable=True),
        sa.Column("phone", sa.String(length=30), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nit_rut"),
        sa.UniqueConstraint("subdomain"),
    )
    op.create_index("ix_companies_id", "companies", ["id"], unique=False)
    op.create_index("ix_companies_nit_rut", "companies", ["nit_rut"], unique=True)
    op.create_index("ix_companies_subdomain", "companies", ["subdomain"], unique=True)

    # 2. Crear tabla 'plans'
    op.create_table(
        "plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("code", sa.String(length=30), nullable=False),
        sa.Column("max_branches", sa.Integer(), server_default="2", nullable=False),
        sa.Column("has_ai_access", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("price_monthly", sa.Numeric(precision=10, scale=2), server_default="0.0", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_plans_id", "plans", ["id"], unique=False)

    # 3. Crear tabla 'subscriptions'
    op.create_table(
        "subscriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("plan_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("start_date", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=20), server_default="ACTIVA", nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["plan_id"], ["plans.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_subscriptions_id", "subscriptions", ["id"], unique=False)
    op.create_index("ix_subscriptions_company_id", "subscriptions", ["company_id"], unique=False)
    op.create_index("ix_subscriptions_plan_id", "subscriptions", ["plan_id"], unique=False)

    # 4. Modificar tipo enum rolenum para admitir 'superadmin' si existe
    try:
        op.execute("ALTER TYPE rolenum ADD VALUE IF NOT EXISTS 'superadmin'")
    except Exception:
        pass

    try:
        op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now()")
    except Exception:
        pass

    # 5. Agregar tenant_id a la tabla 'users'
    op.add_column("users", sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key("fk_users_tenant_id", "users", "companies", ["tenant_id"], ["id"], ondelete="CASCADE")
    op.create_index("ix_users_tenant_id", "users", ["tenant_id"], unique=False)

    # 6. Agregar tenant_id a la tabla 'branches'
    op.add_column("branches", sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key("fk_branches_tenant_id", "branches", "companies", ["tenant_id"], ["id"], ondelete="CASCADE")
    op.create_index("ix_branches_tenant_id", "branches", ["tenant_id"], unique=False)


def downgrade() -> None:
    # 1. Remover tenant_id de branches
    op.drop_index("ix_branches_tenant_id", table_name="branches")
    op.drop_constraint("fk_branches_tenant_id", "branches", type_="foreignkey")
    op.drop_column("branches", "tenant_id")

    # 2. Remover tenant_id de users
    op.drop_index("ix_users_tenant_id", table_name="users")
    op.drop_constraint("fk_users_tenant_id", "users", type_="foreignkey")
    op.drop_column("users", "tenant_id")

    # 3. Eliminar subscriptions
    op.drop_index("ix_subscriptions_plan_id", table_name="subscriptions")
    op.drop_index("ix_subscriptions_company_id", table_name="subscriptions")
    op.drop_index("ix_subscriptions_id", table_name="subscriptions")
    op.drop_table("subscriptions")

    # 4. Eliminar plans
    op.drop_index("ix_plans_id", table_name="plans")
    op.drop_table("plans")

    # 5. Eliminar companies
    op.drop_index("ix_companies_subdomain", table_name="companies")
    op.drop_index("ix_companies_nit_rut", table_name="companies")
    op.drop_index("ix_companies_id", table_name="companies")
    op.drop_table("companies")
