# Re-export from canonical package location for backward compatibility
from app.packages.p1_gestion_usuarios_acceso.routes.user_routes import (
    create_admin_user_route,
    create_user_route,
    delete_user_route,
    get_me_route,
    get_user_route,
    get_users_route,
    router,
    update_me_route,
    update_user_active_route,
    update_user_branch_route,
    update_user_full_route,
    update_user_rol_route,
)

__all__ = [
    "create_admin_user_route",
    "create_user_route",
    "delete_user_route",
    "get_me_route",
    "get_user_route",
    "get_users_route",
    "router",
    "update_me_route",
    "update_user_active_route",
    "update_user_branch_route",
    "update_user_full_route",
    "update_user_rol_route",
]
