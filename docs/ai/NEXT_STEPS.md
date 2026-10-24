# NEXT STEPS — FASHIONSTORE SAAS MULTITENANT

## Tareas Inmediatas de Implementación (Presentación 1: 25/10/2026)

### Hito 1: Núcleo SaaS Multitenant y Aislamiento por Empresa
1. **Paquete `backend/app/packages/p0_saas_plataforma/`:**
   - [x] Modelos SQLAlchemy: `Company`, `Plan`, `Subscription`.
   - [x] Schemas Pydantic: `CompanyCreate`, `CompanyRead`, `PlanRead`, `SubscriptionCreate`.
   - [x] Servicios: `tenant_service.py` (crear empresa y administrador inicial) y `quota_service.py` (validar límite de sucursales).
   - [x] Router `p0_router`: Montar `/api/saas/companies`, `/api/saas/plans` y `/api/saas/subscriptions` en `main.py`.
2. **Implementar Aislamiento por Tenant:**
   - [x] Crear `backend/app/core/tenant_context.py` con dependencias FastAPI para resolver `tenant_id`.
   - [x] Añadir columna `tenant_id` a `users` y `branches`.
   - [x] Actualizar login JWT en `p1_gestion_usuarios_acceso/routes/auth.py` para emitir token con claim `tenant_id`.
3. **Persistencia y Población de Datos Inicial (Migración & Seeders):**
   - [x] Crear migración Alembic `0038_add_saas_multitenant_tables.py` y ejecutar `alembic upgrade head`.
   - [x] Script de seed con 2 planes: Básico (máx. 2 sucursales) y Profesional (máx. 10 sucursales).
   - [x] Alta de 2 empresas de prueba independientes: "Boutique Elegance" y "Moda Urbana" con sus respectivos administradores y sucursales.
   - [x] Alta del Superadministrador global (`superadmin@fashionstore.com`).
4. **Frontend Master Portal (Superadmin - CU01 Completado):**
   - [x] Servicio Angular para consumir API de tenants (`/api/saas/companies`).
   - [x] Vista en Angular para listado y alta reactiva de empresas tenants (CU01).
   - [x] Asignación de plan de suscripción comercial (CU02).

### Hito 2: Persistencia Local del Catálogo (PWA e IndexedDB)
1. **Frontend PWA:**
   - [ ] Configurar `@angular/pwa`, Service Worker y Web App Manifest.
   - [ ] Crear `src/app/core/offline/idb.service.ts` para almacenar catálogo de prendas y existencias conocidas.
   - [ ] Agregar detector de conexión (`online` / `offline`) y banner visual con advertencia de datos locales.

### Hito 3: Persistencia Local en Móvil (Flutter + SQLite)
1. **Mobile SQLite:**
   - [ ] Configurar `sqflite` y crear `local_database.dart`.
   - [ ] Descarga y almacenamiento del catálogo para consulta sin internet.
