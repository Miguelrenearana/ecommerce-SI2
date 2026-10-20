"""Paquete 2 – Gestión de productos y catálogo (CU07–CU10)

Cubre:
- CU07: Registrar y enviar información de productos
- CU08: Gestionar catálogo y productos
- CU09: Gestionar atributos del catálogo
- CU10: Consultar y filtrar catálogo
"""

from app.packages.p2_gestion_productos_catalogo.router import p2_router

__all__ = ["p2_router"]
