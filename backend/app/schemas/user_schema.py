# Re-export from canonical package location for backward compatibility
from app.packages.p1_gestion_usuarios_acceso.schemas.user_schema import (
    AdminUserCreate,
    UserActiveUpdate,
    UserCreate,
    UserLogin,
    UserOut,
    UserProfileUpdate,
    UserRead,
    UsersPaginatedResponse,
    UserUpdate,
    UserUpdateBranch,
    UserUpdateRol,
)

__all__ = [
    "AdminUserCreate",
    "UserActiveUpdate",
    "UserCreate",
    "UserLogin",
    "UserOut",
    "UserProfileUpdate",
    "UserRead",
    "UsersPaginatedResponse",
    "UserUpdate",
    "UserUpdateBranch",
    "UserUpdateRol",
]
