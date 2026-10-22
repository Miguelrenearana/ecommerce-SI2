from app.packages.p1_gestion_usuarios_acceso.routes.auth import router as auth_router
from app.packages.p1_gestion_usuarios_acceso.routes.user_routes import router as user_router
from app.packages.p1_gestion_usuarios_acceso.routes.branch_routes import router as branch_router
from app.packages.p1_gestion_usuarios_acceso.routes.provider_routes import router as provider_router

__all__ = [
    "auth_router",
    "user_router",
    "branch_router",
    "provider_router",
]
