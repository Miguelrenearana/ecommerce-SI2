from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.packages.p0_saas_plataforma.models.subscription import Subscription
from app.packages.p0_saas_plataforma.models.plan import Plan
from app.packages.p0_saas_plataforma.models.company import Company
from app.packages.p0_saas_plataforma.schemas.subscription_schema import (
    SubscriptionCreate,
    SubscriptionRead,
)
from app.packages.p0_saas_plataforma.services.quota_service import get_active_subscription
from app.packages.p1_gestion_usuarios_acceso.models.branch import Branch
from app.utils.response import response

router = APIRouter(prefix="/saas/subscriptions", tags=["SaaS Subscriptions"])


@router.get("/company/{company_id}", summary="Obtener suscripción activa de una empresa")
def get_company_subscription(company_id: UUID, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empresa {company_id} no encontrada",
        )

    sub = get_active_subscription(db, company_id)
    if not sub:
        return response(
            status_code=status.HTTP_200_OK,
            message="La empresa no cuenta con una suscripción activa",
            data=None,
        )

    return response(
        status_code=status.HTTP_200_OK,
        message="Suscripción activa encontrada",
        data=SubscriptionRead.model_validate(sub).model_dump(),
    )


@router.post("", summary="Asignar o cambiar suscripción de una empresa")
def assign_subscription(sub_in: SubscriptionCreate, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == sub_in.company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empresa {sub_in.company_id} no encontrada",
        )

    plan = db.query(Plan).filter(Plan.id == sub_in.plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan {sub_in.plan_id} no encontrado",
        )

    # Validar que si se degrada el plan, la empresa no tenga más sucursales activas que el nuevo límite
    active_branches = (
        db.query(Branch)
        .filter(Branch.tenant_id == company.id, Branch.is_active.is_(True))
        .count()
    )
    if active_branches > plan.max_branches:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede cambiar al plan {plan.name}. La empresa tiene {active_branches} sucursales activas y el plan permite un máximo de {plan.max_branches}.",
        )

    # Marcar suscripciones anteriores como CANCELADA
    prev_subs = db.query(Subscription).filter(
        Subscription.company_id == company.id,
        Subscription.status == "ACTIVA",
    ).all()
    for s in prev_subs:
        s.status = "CANCELADA"

    # Crear nueva suscripción
    new_sub = Subscription(
        company_id=company.id,
        plan_id=plan.id,
        end_date=sub_in.end_date,
        status=sub_in.status,
    )
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)

    return response(
        status_code=status.HTTP_201_CREATED,
        message=f"Plan {plan.name} asignado exitosamente a la empresa",
        data=SubscriptionRead.model_validate(new_sub).model_dump(),
    )
