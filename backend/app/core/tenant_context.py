from uuid import UUID
from fastapi import Header, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.packages.p0_saas_plataforma.models.company import Company


def get_tenant_id_from_header(
    x_tenant_id: str | None = Header(None, alias="X-Tenant-ID"),
    x_tenant_subdomain: str | None = Header(None, alias="X-Tenant-Subdomain"),
    db: Session = Depends(get_db),
) -> UUID | None:
    """
    Resuelve el tenant_id opcional a partir de los headers HTTP:
    1. 'X-Tenant-ID' (UUID de la empresa)
    2. 'X-Tenant-Subdomain' (Slug del tenant)
    """
    if x_tenant_id:
        try:
            tenant_uuid = UUID(x_tenant_id)
            company = db.query(Company).filter(Company.id == tenant_uuid).first()
            if not company:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Empresa tenant con ID '{x_tenant_id}' no existe.",
                )
            if company.status != "ACTIVO":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="La empresa tenant se encuentra suspendida.",
                )
            return company.id
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El header 'X-Tenant-ID' debe ser un UUID válido.",
            ) from exc

    if x_tenant_subdomain:
        subdomain_clean = x_tenant_subdomain.strip().lower()
        company = db.query(Company).filter(Company.subdomain == subdomain_clean).first()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empresa tenant con subdominio '{x_tenant_subdomain}' no existe.",
            )
        if company.status != "ACTIVO":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="La empresa tenant se encuentra suspendida.",
            )
        return company.id

    return None


def require_tenant_id(
    tenant_id: UUID | None = Depends(get_tenant_id_from_header),
) -> UUID:
    """
    Dependencia obligatoria para endpoints que exigen contexto tenant.
    """
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se requiere especificar el tenant mediante el header 'X-Tenant-ID' o 'X-Tenant-Subdomain'.",
        )
    return tenant_id


def get_current_tenant(
    tenant_id: UUID = Depends(require_tenant_id),
    db: Session = Depends(get_db),
) -> Company:
    """
    Retorna la entidad Company correspondiente al tenant actual.
    """
    company = db.query(Company).filter(Company.id == tenant_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa tenant no encontrada.",
        )
    return company
