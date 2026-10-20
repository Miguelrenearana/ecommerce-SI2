from app.core.database import SessionLocal
from app.packages.p4_gestion_compras_reservas.services.order_service import expire_due_orders
from app.packages.p4_gestion_compras_reservas.services.reservation_service import (
    expire_due_reservations,
    expire_transferred_reservations,
)


def run_daily_expiration() -> None:
    db = SessionLocal()
    try:
        expire_due_reservations(db)
        expire_due_orders(db)
        expire_transferred_reservations(db)
    finally:
        db.close()
