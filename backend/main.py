import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.packages.p1_gestion_usuarios_acceso import p1_router
from app.packages.p2_gestion_productos_catalogo import p2_router
from app.packages.p3_gestion_inventario_disponibilidad import p3_router
from app.packages.p4_gestion_compras_reservas import p4_router
from app.packages.p5_gestion_ventas_pos import p5_router
from app.routes import report_routes, dashboard_routes, recommendation_routes, chatbot_routes, notification_routes
from app.core.error_handlers import register_error_handlers
from app.core.database import SessionLocal
from app.services.expiration_service import run_daily_expiration
from app.services.order_service import expire_due_orders


async def _expire_orders_loop() -> None:
    while True:
        await asyncio.sleep(60)
        db = SessionLocal()
        try:
            expire_due_orders(db)
        except Exception:
            db.rollback()
        finally:
            db.close()


async def _daily_expiration_loop() -> None:
    while True:
        now = datetime.now()
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        await asyncio.sleep(max((next_midnight - now).total_seconds(), 1))
        try:
            run_daily_expiration()
        except Exception:
            pass


@asynccontextmanager
async def lifespan(_: FastAPI):
    task = asyncio.create_task(_expire_orders_loop())
    daily_task = asyncio.create_task(_daily_expiration_loop())
    try:
        yield
    finally:
        task.cancel()
        daily_task.cancel()
        await asyncio.gather(task, daily_task, return_exceptions=True)

app = FastAPI(title="ACI", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
api_router = APIRouter(prefix="/api")
# Paquete 1: Gestión de usuarios y acceso (CU01–CU06)
api_router.include_router(p1_router)



# Paquete 2: Gestión de productos y catálogo (CU07–CU10)
api_router.include_router(p2_router)

# Paquete 3: Gestión de inventario y disponibilidad (CU11–CU13)
api_router.include_router(p3_router)
# Paquete 4: Gestión de compras y reservas (CU14–CU16, CU25)
api_router.include_router(p4_router)



# Paquete 5: Ventas y POS (CU17–CU18)
api_router.include_router(p5_router)
api_router.include_router(report_routes.router)
api_router.include_router(dashboard_routes.router)


api_router.include_router(recommendation_routes.router)
api_router.include_router(chatbot_routes.router)
api_router.include_router(notification_routes.router)

app.include_router(api_router)

register_error_handlers(app)
