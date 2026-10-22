# Re-export from canonical package location for backward compatibility
from app.packages.p1_gestion_usuarios_acceso.models.user import User, Base, UserBodyProfile

__all__ = ["User", "Base", "UserBodyProfile"]
