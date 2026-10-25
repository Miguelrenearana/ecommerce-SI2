# CURRENT STATE — FASHIONSTORE SAAS MULTITENANT

## Estado Consolidado del Proyecto (24 de Octubre de 2026)

### 1. Resumen de Casos de Uso (Total: 28 CUs)
* **Casos de Uso del 1er Parcial (Modificados/Preservados):** 12 CUs (Base operativa lista; con `tenant_id` y aislamiento en base de datos activo).
* **Casos de Uso Exclusivos del 2do Parcial (Nuevos/Extras):** 16 CUs (En proceso de implementación incremental).
* **Progreso Global del 2do Parcial:** CU01 (Tenants) y CU02 (Planes de Suscripción y Límites Comerciales) cuentan con Backend, Persistencia PostgreSQL y Frontend Web en Angular 21 100% operativos y verificados.

---

### 2. Estado por Componente Arquitectónico

#### Base de Datos (PostgreSQL 15+)
* **Migraciones 0038 y 0039 Aplicadas:** Tablas `companies`, `plans` y `subscriptions` creadas y enriquecidas con descripciones comerciales y campos de auditoría; foráneas `tenant_id` añadidas a `users` y `branches`.
* **Datos Sembrados (`seed_saas.py`):**
  - Planes: `BASICO` (2 sucursales, sin IA, $29/mes) y `PROFESIONAL` (10 sucursales, con IA, $99/mes).
  - Superadmin Global: `superadmin@fashionstore.com`.
  - 2 Tenants Activos: "Boutique Elegance" (Plan Pro, 2 sucursales) y "Moda Urbana" (Plan Básico, 1 sucursal).

#### Backend (FastAPI + SQLAlchemy)
* **Estructura:** Modularizada en 7 paquetes de dominio autónomos (`p0_saas_plataforma` a `p6_inteligencia_analitica`).
* **Endpoints:** 105+ rutas REST verificadas en la especificación OpenAPI de Swagger (incluyendo `/api/saas/companies`, `/api/saas/plans` y `/api/saas/subscriptions`).
* **Aislamiento Multitenant & Cuotas:** Middleware `tenant_context.py` y reglas comerciales en `quota_service.py` activas con *Downgrade Guard*.

#### Frontend Web (Angular 21 PWA)
* **Estructura:** Organizada por roles (`features/superadmin/`, `features/cliente/`, `features/admin/`, `features/cajero/`, `features/encargado/`, `features/proveedor/`).
* **Portal Master Superadmin (CU01 y CU02 Implementados):**
  - Modelos y servicios en [`frontend/src/app/core/services/company.service.ts`](file:///c:/Users/PERSONAL/ecommerce-SI2/frontend/src/app/core/services/company.service.ts) (CRUD de tenants, gestión de suscripciones y cambio reactivo de planes).
  - Vistas y modales: [`tenants-page.component.ts`](file:///c:/Users/PERSONAL/ecommerce-SI2/frontend/src/app/features/superadmin/pages/tenants-page.component.ts), modal de alta de tenant y modal de gestión de suscripciones con *Downgrade Guard*.
  - Ruta protegida `/app/superadmin/tenants` con `roleGuard(['superadmin'])`.
* **Pendiente Inmediato:** Service Worker e IndexedDB para catálogo offline (CU08/CU09) y validación de creación de sucursales según plan (CU04).

#### Aplicación Móvil (Flutter / Dart)
* **Estructura:** `mobile/lib/` con features desacopladas.
* **Pendiente Inmediato:** Integración de persistencia local en SQLite (`sqflite`), mapa con OpenStreetMap (`flutter_map`) y cola de sincronización offline.
