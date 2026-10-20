"""Paquete 1 – Gestión de usuarios y acceso (CU01–CU06)

Cubre:
- CU01: Registrar cliente
- CU02: Iniciar sesión
- CU03: Gestionar usuarios internos
- CU04: Gestionar sucursales
- CU05: Gestionar cuentas de proveedor
- CU06: Consultar y actualizar perfil
"""

from app.packages.p1_gestion_usuarios_acceso.router import p1_router

__all__ = ["p1_router"]
