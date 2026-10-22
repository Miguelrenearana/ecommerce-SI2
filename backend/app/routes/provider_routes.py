# Re-export from canonical package location for backward compatibility
from app.packages.p1_gestion_usuarios_acceso.routes.provider_routes import (
    create_provider_route,
    delete_provider_route,
    list_my_products,
    list_provider_products_route,
    list_providers_route,
    router,
    update_my_availability,
    update_provider_full_route,
    update_provider_status_route,
)

__all__ = [
    "create_provider_route",
    "delete_provider_route",
    "list_my_products",
    "list_provider_products_route",
    "list_providers_route",
    "router",
    "update_my_availability",
    "update_provider_full_route",
    "update_provider_status_route",
]
