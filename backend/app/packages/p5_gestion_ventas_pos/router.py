from fastapi import APIRouter

from app.packages.p5_gestion_ventas_pos.routes.sales_routes import router as sales_router

p5_router = APIRouter()
p5_router.include_router(sales_router)

__all__ = ["p5_router"]
