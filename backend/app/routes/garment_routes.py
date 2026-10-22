# Re-export from canonical package location for backward compatibility
from app.packages.p2_gestion_productos_catalogo.routes.garment_routes import (
    catalog_garment_route,
    router,
)

__all__ = ["catalog_garment_route", "router"]
