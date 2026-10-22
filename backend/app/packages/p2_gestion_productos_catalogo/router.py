from fastapi import APIRouter

from app.packages.p2_gestion_productos_catalogo.routes.catalog_routes import router as catalog_router
from app.packages.p2_gestion_productos_catalogo.routes.garment_routes import router as garment_router

# Router unificado del Paquete 2: Gestión de productos y catálogo
p2_router = APIRouter()
p2_router.include_router(catalog_router)
p2_router.include_router(garment_router)
