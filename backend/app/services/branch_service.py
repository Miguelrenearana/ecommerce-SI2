# Re-export from canonical package location for backward compatibility
from app.packages.p1_gestion_usuarios_acceso.services.branch_service import (
    create_branch,
    delete_branch,
    get_branch_quota,
    get_branches,
    set_branch_active,
    update_branch,
    validate_branch_quota,
)

__all__ = [
    "create_branch",
    "delete_branch",
    "get_branch_quota",
    "get_branches",
    "set_branch_active",
    "update_branch",
    "validate_branch_quota",
]
