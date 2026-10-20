# Re-export from canonical package location for backward compatibility
from app.packages.p1_gestion_usuarios_acceso.routes.auth import router, register, login

__all__ = ["router", "register", "login"]
