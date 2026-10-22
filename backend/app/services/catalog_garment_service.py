# Re-export from canonical package location for backward compatibility
from app.packages.p2_gestion_productos_catalogo.services.catalog_garment_service import (
    CatalogGarmentError,
    generate_catalog_garment,
)

__all__ = ["CatalogGarmentError", "generate_catalog_garment"]
