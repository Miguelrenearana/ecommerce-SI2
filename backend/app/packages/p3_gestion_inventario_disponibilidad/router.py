from fastapi import APIRouter
from app.packages.p3_gestion_inventario_disponibilidad.routes.inventory_routes import (
    router as inventory_router,
)
from app.packages.p3_gestion_inventario_disponibilidad.routes.replenishment_routes import (
    router as replenishment_router,
)

p3_router = APIRouter()
p3_router.include_router(inventory_router)
p3_router.include_router(replenishment_router)

__all__ = ["p3_router"]
