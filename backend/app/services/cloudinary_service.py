# Re-export from canonical package location for backward compatibility
from app.packages.p2_gestion_productos_catalogo.services.cloudinary_service import (
    delete_image,
    upload_image,
)

__all__ = ["delete_image", "upload_image"]
