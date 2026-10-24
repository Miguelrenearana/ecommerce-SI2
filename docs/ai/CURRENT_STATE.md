# CURRENT STATE — FASHIONSTORE SAAS MULTITENANT

## Estado Consolidado del Proyecto (24 de Octubre de 2026)

### 1. Resumen de Casos de Uso (Total: 28 CUs)
* **Casos de Uso del 1er Parcial (Modificados/Preservados):** 12 CUs (Base operativa lista; requieren inyección de `tenant_id` y aislamiento).
* **Casos de Uso Exclusivos del 2do Parcial (Nuevos/Extras):** 16 CUs (En proceso de implementación incremental).
* **Progreso Global del 2do Parcial:** 12 de 28 Casos de Uso con base funcional operativa (~42.8%).

---

### 2. Estado por Componente Arquitectónico

#### Backend (FastAPI + PostgreSQL 15+)
* **Estructura:** Modularizada en paquetes de dominio autónomos (`p1` a `p6`).
* **Endpoints:** 96 rutas REST verificadas en la especificación OpenAPI de Swagger.
* **Pendiente Inmediato:** Creación del paquete `p0_saas_platform`, middleware de aislamiento de tenant (`app/core/tenant_context.py`), migración de columna `tenant_id` y validación de cuotas comerciales de suscripción (2 vs 10 sucursales).

#### Frontend Web (Angular 21 PWA)
* **Estructura:** Organizada por roles (`features/cliente/`, `features/admin/`, `features/cajero/`, `features/encargado/`, `features/proveedor/`).
* **Dependencias:** `node_modules` instalados y saneados con `npm install --legacy-peer-deps`.
* **Pendiente Inmediato:** Service Worker (`@angular/pwa`), almacenamiento local del catálogo con IndexedDB y banner de modo offline.

#### Aplicación Móvil (Flutter / Dart)
* **Estructura:** `mobile/lib/` con features desacopladas.
* **Pendiente Inmediato:** Integración de persistencia local en SQLite (`sqflite`), mapa con OpenStreetMap (`flutter_map`) y cola de sincronización offline.

#### Base de Datos (PostgreSQL)
* **Esquema:** Tablas relacionales del 1er parcial completas (usuarios, sucursales, productos, variantes, inventarios, ventas, reservas, órdenes).
* **Pendiente Inmediato:** Migración de nuevas entidades SaaS (`companies`, `plans`, `subscriptions`), tablas de offline/sync (`sync_operations`, `sync_conflicts`) y devoluciones/cambios (`garment_exchanges`, `garment_returns`).
