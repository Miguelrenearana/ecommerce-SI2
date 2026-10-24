from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class CompanyBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150, description="Nombre comercial")
    business_name: str = Field(..., min_length=2, max_length=200, description="Razón social oficial")
    nit_rut: str = Field(..., min_length=3, max_length=50, description="NIT o RUT de la empresa")
    subdomain: str = Field(..., min_length=2, max_length=63, pattern=r"^[a-z0-9-]+$", description="Slug del tenant (minúsculas, números y guiones)")
    email: EmailStr | None = None
    phone: str | None = None


class CompanyCreate(CompanyBase):
    plan_code: str = Field("basic", description="Código del plan inicial: 'basic' o 'pro'")
    admin_name: str | None = Field(None, description="Nombre del administrador inicial del tenant")
    admin_email: EmailStr | None = Field(None, description="Correo del administrador inicial")
    admin_password: str | None = Field(None, min_length=8, description="Contraseña del administrador inicial")


class CompanyUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=150)
    business_name: str | None = Field(None, min_length=2, max_length=200)
    email: EmailStr | None = None
    phone: str | None = None


class CompanyStatusUpdate(BaseModel):
    status: str = Field(..., pattern=r"^(ACTIVO|SUSPENDIDO)$", description="Estado de la empresa")


class CompanyRead(CompanyBase):
    id: UUID
    status: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class CompanyOut(BaseModel):
    company: CompanyRead
    initial_admin_id: UUID | None = None
    initial_admin_email: str | None = None
