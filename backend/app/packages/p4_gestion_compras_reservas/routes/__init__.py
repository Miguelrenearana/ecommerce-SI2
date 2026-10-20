from app.packages.p4_gestion_compras_reservas.routes.cart_routes import router as cart_router
from app.packages.p4_gestion_compras_reservas.routes.order_routes import router as order_router
from app.packages.p4_gestion_compras_reservas.routes.payment_routes import router as payment_router
from app.packages.p4_gestion_compras_reservas.routes.promotion_routes import router as promotion_router
from app.packages.p4_gestion_compras_reservas.routes.reservation_routes import router as reservation_router

__all__ = [
    "cart_router",
    "order_router",
    "payment_router",
    "promotion_router",
    "reservation_router",
]
