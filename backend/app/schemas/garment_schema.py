# Re-export from canonical package location for backward compatibility
from app.packages.p2_gestion_productos_catalogo.schemas.garment_schema import (
    CatalogGarmentRequest,
    CatalogGarmentResponse,
)

__all__ = ["CatalogGarmentRequest", "CatalogGarmentResponse"]
