from app.packages.p2_gestion_productos_catalogo.routes.catalog_routes import router as catalog_router
from app.packages.p2_gestion_productos_catalogo.routes.garment_routes import router as garment_router

__all__ = [
    "catalog_router",
    "garment_router",
]
