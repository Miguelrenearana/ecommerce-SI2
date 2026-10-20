# Re-export from canonical package location for backward compatibility
from app.packages.p1_gestion_usuarios_acceso.models.user_profile import UserBodyProfile

__all__ = ["UserBodyProfile"]
