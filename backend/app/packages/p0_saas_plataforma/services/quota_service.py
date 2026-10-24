from uuid import UUID
from sqlalchemy.orm import Session

from app.packages.p0_saas_plataforma.models.subscription import Subscription
from app.packages.p0_saas_plataforma.models.plan import Plan
from app.packages.p1_gestion_usuarios_acceso.models.branch import Branch


class QuotaExceededException(Exception):
    def __init__(self, message: str, current_count: int, max_allowed: int):
        super().__init__(message)
        self.current_count = current_count
        self.max_allowed = max_allowed


class FeatureNotAllowedException(Exception):
    def __init__(self, message: str, required_plan: str):
        super().__init__(message)
        self.required_plan = required_plan


def get_active_subscription(db: Session, company_id: UUID) -> Subscription | None:
    return (
        db.query(Subscription)
        .filter(Subscription.company_id == company_id, Subscription.status == "ACTIVA")
        .order_by(Subscription.start_date.desc())
        .first()
    )


def validate_branch_quota(db: Session, company_id: UUID) -> tuple[int, int]:
    """
    Valida si la empresa puede crear una nueva sucursal según su plan de suscripción.
    - Plan Básico: máximo 2 sucursales.
    - Plan Profesional: máximo 10 sucursales.
    Lanza QuotaExceededException si ya alcanzó el límite.
    """
    subscription = get_active_subscription(db, company_id)
    if not subscription or not subscription.plan:
        max_branches = 2  # Por defecto cuota mínima básica
    else:
        max_branches = subscription.plan.max_branches

    # Contar sucursales activas de este tenant
    active_branches_count = (
        db.query(Branch)
        .filter(Branch.tenant_id == company_id, Branch.is_active.is_(True))
        .count()
    )

    if active_branches_count >= max_branches:
        plan_name = subscription.plan.name if subscription and subscription.plan else "Básico"
        raise QuotaExceededException(
            message=f"Límite de sucursales alcanzado para el plan {plan_name}. "
                    f"Activas: {active_branches_count}, Permitidas: {max_branches}. "
                    "Actualice a Plan Profesional para habilitar hasta 10 sucursales.",
            current_count=active_branches_count,
            max_allowed=max_branches,
        )

    return active_branches_count, max_branches


def validate_ai_access(db: Session, company_id: UUID) -> bool:
    """
    Valida si la empresa tiene habilitado el módulo de IA y analítica predictiva.
    - Plan Básico: Sin IA.
    - Plan Profesional: Con IA (Gemini RAG y Machine Learning).
    """
    subscription = get_active_subscription(db, company_id)
    if not subscription or not subscription.plan or not subscription.plan.has_ai_access:
        raise FeatureNotAllowedException(
            message="El módulo de Inteligencia Artificial (Gemini y Machine Learning) "
                    "requiere una suscripción activa a Plan Profesional.",
            required_plan="PROFESIONAL",
        )
    return True
