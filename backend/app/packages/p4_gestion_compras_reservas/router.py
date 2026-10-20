from fastapi import APIRouter

from app.packages.p4_gestion_compras_reservas.routes.cart_routes import router as cart_router
from app.packages.p4_gestion_compras_reservas.routes.order_routes import router as order_router
from app.packages.p4_gestion_compras_reservas.routes.payment_routes import router as payment_router
from app.packages.p4_gestion_compras_reservas.routes.promotion_routes import router as promotion_router
from app.packages.p4_gestion_compras_reservas.routes.reservation_routes import router as reservation_router


p4_router = APIRouter()
p4_router.include_router(cart_router)
p4_router.include_router(reservation_router)
p4_router.include_router(order_router)
p4_router.include_router(payment_router)
p4_router.include_router(promotion_router)

__all__ = ["p4_router"]
