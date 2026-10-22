# Re-export from canonical package location for backward compatibility
from app.packages.p2_gestion_productos_catalogo.models.product import Product

__all__ = ["Product"]
