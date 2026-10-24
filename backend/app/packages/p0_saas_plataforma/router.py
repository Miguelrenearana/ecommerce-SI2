from fastapi import APIRouter

from app.packages.p0_saas_plataforma.routes.company_routes import router as company_router
from app.packages.p0_saas_plataforma.routes.plan_routes import router as plan_router
from app.packages.p0_saas_plataforma.routes.subscription_routes import router as subscription_router

# Router unificado del Paquete 0: Plataforma SaaS, Gestión de Tenants y Suscripciones
p0_router = APIRouter()
p0_router.include_router(company_router)
p0_router.include_router(plan_router)
p0_router.include_router(subscription_router)
