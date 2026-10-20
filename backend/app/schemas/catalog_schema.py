# Re-export from canonical package location for backward compatibility
from app.packages.p2_gestion_productos_catalogo.schemas.catalog_schema import (
    CollectionCreate,
    ColorCreate,
    DiscountTypeEnum,
    NameCreate,
    Point,
    ProductCreate,
    ProductRead,
    ProductVariantCreate,
    ProductVariantGarmentPointsUpdate,
    ProductVariantRead,
    ProductVariantStatusUpdate,
)

__all__ = [
    "CollectionCreate",
    "ColorCreate",
    "DiscountTypeEnum",
    "NameCreate",
    "Point",
    "ProductCreate",
    "ProductRead",
    "ProductVariantCreate",
    "ProductVariantGarmentPointsUpdate",
    "ProductVariantRead",
    "ProductVariantStatusUpdate",
]
