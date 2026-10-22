# Re-export from canonical package location for backward compatibility
from app.packages.p1_gestion_usuarios_acceso.schemas.branch_schema import (
    BranchActiveUpdate,
    BranchCreate,
    BranchRead,
    BranchUpdate,
)

__all__ = [
    "BranchActiveUpdate",
    "BranchCreate",
    "BranchRead",
    "BranchUpdate",
]
