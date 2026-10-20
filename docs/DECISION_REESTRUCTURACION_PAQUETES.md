# Decisión de Arquitectura: Reestructuración por Paquetes de Dominio (Backend)

**Fecha:** 20 de Octubre de 2026  
**Estado:** Aprobado / En Implementación  
**Contexto:** Preparación y estabilización de la base arquitectónica previa a la transición hacia **ICONIX** y **SaaS Multitenant** (Examen Parcial 2).

---

## 1. Contexto y Problema

El backend de FashionStore fue organizado inicialmente mediante el patrón *Package by Layer* horizontal:
```
backend/app/
├── models/
├── routes/
├── schemas/
└── services/
```

Si bien esta estructura fue suficiente para el prototipo inicial, presenta limitaciones de cara a la evolución del sistema:
1. **Falta de Localidad (*Locality*):** Cualquier cambio sobre un caso de uso requiere modificar archivos distribuidos en 4 carpetas distintas.
2. **Preparación para Multitenancy (Parcial 2):** La transformación a SaaS exige incorporar el aislamiento por tenant (`tenant_id`), suscripciones, sincronización offline y gestión de cambios de prendas sin que la base de código colapse en acoplamientos cruzados.
3. **Trazabilidad con ICONIX y PUDS:** El informe de arquitectura define formalmente **6 paquetes de análisis (P1 a P6)** según afinidad funcional y casos de uso (CU01–CU25).

---

## 2. Decisión Arquitectónica

Se adopta una **Arquitectura por Paquetes de Dominio** orientada a **Módulos Profundos (*Deep Modules*)** bajo los principios de `codebase-design`:

### 2.1. Nombres y Alcance de los Paquetes (en Español)
Los nombres de las carpetas reflejan fielmente los paquetes definidos en la documentación oficial:

| Paquete | Casos de Uso | Descripción de Alcance |
|---|---|---|
| **`p1_gestion_usuarios_acceso`** | CU01–CU06 | Registro, autenticación JWT, usuarios internos, sucursales, proveedores y perfil. |
| **`p2_gestion_productos_catalogo`** | CU07–CU10 | Productos, variantes, atributos (tallas, colores, temporadas, colecciones) y envíos de proveedor. |
| **`p3_gestion_inventario_disponibilidad`** | CU11–CU13 | Stock por sucursal, movimientos (ingreso, salida, traspaso) y consolidado. |
| **`p4_gestion_compras_reservas`** | CU14–CU16, CU25 | Carrito de compras, reservas de cliente, órdenes, pagos electrónicos (Stripe/efectivo) y cupones. |
| **`p5_gestion_ventas_sucursal`** | CU17–CU18 | Atención de reservas en tienda física y punto de venta presencial (POS). *Se extenderá en Parcial 2 con offline sync y cambios de prenda.* |
| **`p6_experiencia_inteligente_analitica`** | CU19–CU24 | Vestidor virtual AR, recomendaciones IA (ALS), chatbot Gemini, reportes por voz y notificaciones push. |
| **`p0_saas_multitenant`** *(Futuro Parcial 2)* | Requisitos SaaS | Empresas (tenants), planes de suscripción, cuotas y control de acceso multitenant. |

### 2.2. Rechazo de Micro-Subcarpetas / Subapps Innecesarias
Se evaluó y **descartó** la subdivisión de cada paquete en micro-carpetas por entidad (p. ej. `p1/users/`, `p1/roles/`, `p1/branches/`).
- **Motivo:** Produce módulos poco profundos (*shallow modules*), explosión de archivos con pocas líneas, e incurre en problemas recurrentes de **importaciones circulares** en Python/SQLAlchemy (ej. `User` referencia a `Branch` y `Branch` referencia a `User`).
- **Solución elegida:** Cada paquete agrupa cohesivamente sus modelos, esquemas, servicios y rutas, ofreciendo una interfaz interna limpia y un enrutador consolidado hacia `main.py`.

---

## 3. Implementación Progresiva y Compatibilidad Inversa

La reestructuración se ejecuta de manera modular, paquete por paquete:

1. **Paquete 1 (`p1_gestion_usuarios_acceso`) - COMPLETADO:**
   `backend/app/packages/p1_gestion_usuarios_acceso/`
   - `models/`: `user.py`, `user_profile.py`, `branch.py`, `provider.py`, `provider_variant_availability.py`.
   - `schemas/`: `user_schema.py`, `branch_schema.py`, `provider_schema.py`, `provider_availability_schema.py`.
   - `services/`: `user_service.py`, `branch_service.py`, `provider_service.py`.
   - `routes/`: `auth.py`, `user_routes.py`, `branch_routes.py`, `provider_routes.py`.
   - `router.py`: Consolida las rutas de P1 bajo un enrutador único `p1_router`.

2. **Paquete 2 (`p2_gestion_productos_catalogo`) - COMPLETADO:**
   `backend/app/packages/p2_gestion_productos_catalogo/`
   - `models/`: `category.py`, `size.py`, `color.py`, `season.py`, `collection.py`, `product.py`, `product_variant.py`.
   - `schemas/`: `catalog_enums.py`, `catalog_schema.py`, `garment_schema.py`.
   - `services/`: `catalog_service.py`, `catalog_garment_service.py`, `cloudinary_service.py`.
   - `routes/`: `catalog_routes.py`, `garment_routes.py`.
   - `router.py`: Consolida las rutas de P2 bajo un enrutador único `p2_router`.

3. **Paquete 3 (`p3_gestion_inventario_disponibilidad`) - COMPLETADO:**
   `backend/app/packages/p3_gestion_inventario_disponibilidad/`
   - `models/`: `inventory.py`, `inventory_movement.py`, `replenishment_request.py`, `replenishment_request_item.py`.
   - `schemas/`: `inventory_schema.py`, `replenishment_schema.py`.
   - `services/`: `inventory_service.py`, `replenishment_service.py`.
   - `routes/`: `inventory_routes.py`, `replenishment_routes.py`.
   - `router.py`: Consolida las rutas de P3 bajo un enrutador único `p3_router`.

4. **Cero Regresiones (Backward-Compatibility Shims):**
   Para evitar roturas en migraciones de Alembic, scripts de carga de datos (`seed.py`) o importaciones en paquetes pendientes de migrar:
   - Los módulos existentes en `app/models/`, `app/schemas/`, `app/services/` y `app/routes/` reexportan transparentemente las definiciones canónicas desde sus respectivos paquetes.
   - Las rutas HTTP expuestas por FastAPI (`/api/inventory`, `/api/replenishment`, etc.) se mantienen 100% idénticas, garantizando impacto cero en Frontend y Mobile.
