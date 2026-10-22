from app.packages.p3_gestion_inventario_disponibilidad.routes.inventory_routes import (
    router as inventory_router,
)
from app.packages.p3_gestion_inventario_disponibilidad.routes.replenishment_routes import (
    router as replenishment_router,
)

__all__ = ["inventory_router", "replenishment_router"]
