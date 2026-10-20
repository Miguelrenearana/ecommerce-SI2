# Re-export from canonical package location for backward compatibility
from app.packages.p1_gestion_usuarios_acceso.services.branch_service import (
    create_branch,
    delete_branch,
    get_branches,
    set_branch_active,
    update_branch,
)

__all__ = [
    "create_branch",
    "delete_branch",
    "get_branches",
    "set_branch_active",
    "update_branch",
]
