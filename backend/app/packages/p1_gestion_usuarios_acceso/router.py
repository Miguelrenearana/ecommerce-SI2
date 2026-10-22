from fastapi import APIRouter

from app.packages.p1_gestion_usuarios_acceso.routes.auth import router as auth_router
from app.packages.p1_gestion_usuarios_acceso.routes.user_routes import router as user_router
from app.packages.p1_gestion_usuarios_acceso.routes.branch_routes import router as branch_router
from app.packages.p1_gestion_usuarios_acceso.routes.provider_routes import router as provider_router

# Router unificado del Paquete 1: Gestión de usuarios y acceso
p1_router = APIRouter()
p1_router.include_router(auth_router)
p1_router.include_router(user_router)
p1_router.include_router(branch_router)
p1_router.include_router(provider_router)
