# Re-export from canonical package location for backward compatibility
from app.packages.p1_gestion_usuarios_acceso.routes.branch_routes import (
    create_branch_route,
    delete_branch_route,
    get_branch_quota_route,
    list_branches_route,
    router,
    update_branch_active_route,
    update_branch_route,
)

__all__ = [
    "create_branch_route",
    "delete_branch_route",
    "get_branch_quota_route",
    "list_branches_route",
    "router",
    "update_branch_active_route",
    "update_branch_route",
]
