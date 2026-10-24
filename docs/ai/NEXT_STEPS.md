# NEXT STEPS — FASHIONSTORE SAAS MULTITENANT

## Tareas Inmediatas de Implementación (Presentación 1: 25/10/2026)

### Hito 1: Núcleo SaaS Multitenant y Aislamiento por Empresa
1. **Crear `backend/app/packages/p0_saas_platform/`:**
   - [ ] Modelos SQLAlchemy: `Company`, `Plan`, `Subscription`.
   - [ ] Schemas Pydantic: `CompanyCreate`, `CompanyRead`, `PlanRead`, `SubscriptionCreate`.
   - [ ] Servicios: `tenant_service.py` (crear empresa y administrador inicial) y `quota_service.py` (validar límite de sucursales).
   - [ ] Router `p0_router`: Montar `/api/saas/companies` y `/api/saas/plans`.
2. **Implementar Aislamiento por Tenant:**
   - [ ] Crear `backend/app/core/tenant_context.py` con dependencia FastAPI para resolver `tenant_id`.
   - [ ] Añadir columna `tenant_id` a `users`, `branches`, `products`, `product_variants`.
   - [ ] Actualizar login JWT en `p1_gestion_usuarios_acceso/routes/auth.py` para emitir token con claim `tenant_id`.
3. **Población de Datos Inicial (Seeders):**
   - [ ] Script de seed con 2 planes: Básico (máx. 2 sucursales) y Profesional (máx. 10 sucursales).
   - [ ] Alta de 2 empresas de prueba independientes: "Boutique Elegance" y "Moda Urbana" con sus respectivos administradores.

### Hito 2: Persistencia Local del Catálogo (PWA e IndexedDB)
1. **Frontend PWA:**
   - [ ] Configurar `@angular/pwa`, Service Worker y Web App Manifest.
   - [ ] Crear `src/app/core/offline/idb.service.ts` para almacenar catálogo de prendas y existencias conocidas.
   - [ ] Agregar detector de conexión (`online` / `offline`) y banner visual con advertencia de datos locales.

### Hito 3: Persistencia Local en Móvil (Flutter + SQLite)
1. **Mobile SQLite:**
   - [ ] Configurar `sqflite` y crear `local_database.dart`.
   - [ ] Descarga y almacenamiento del catálogo para consulta sin internet.
