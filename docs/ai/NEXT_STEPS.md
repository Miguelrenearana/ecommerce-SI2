# NEXT STEPS — FASHIONSTORE SAAS MULTITENANT

## Tareas Inmediatas de Implementación (Presentación 1: 25/10/2026)

### Hito 1: Núcleo SaaS Multitenant y Planes Comerciales (CU01, CU02 & CU04 COMPLETADOS)
1. **Paquete `backend/app/packages/p0_saas_plataforma/`:**
   - [x] Modelos SQLAlchemy: `Company`, `Plan`, `Subscription` con descripciones comerciales y auditoría.
   - [x] Schemas Pydantic: `CompanyCreate`, `CompanyRead`, `PlanRead`, `SubscriptionCreate`.
   - [x] Servicios: `tenant_service.py` y `quota_service.py` (validar límite de sucursales e IA).
   - [x] Router `p0_router`: `/api/saas/companies`, `/api/saas/plans` y `/api/saas/subscriptions` con *Downgrade Guard*.
2. **Implementar Aislamiento por Tenant:**
   - [x] Crear `backend/app/core/tenant_context.py` con dependencias FastAPI para resolver `tenant_id`.
   - [x] Añadir columna `tenant_id` a `users` y `branches`.
   - [x] Actualizar login JWT en `p1_gestion_usuarios_acceso/routes/auth.py` para emitir token con claim `tenant_id`.
3. **Persistencia y Población de Datos Inicial (Migraciones 0038, 0039 y 0040):**
   - [x] Ejecutadas migraciones `0038`, `0039` y `0040` (enriquecimiento de sucursales con coordenadas geo y auditoría).
   - [x] Script de seed con planes Básico ($29) y Profesional ($99).
   - [x] Alta de 2 empresas de prueba: "Boutique Elegance" y "Moda Urbana".
   - [x] Alta del Superadministrador global (`superadmin@fashionstore.com`).
4. **Frontend Master Portal (Superadmin - CU01 y CU02 Completados):**
   - [x] Servicio Angular `company.service.ts` con consumo de empresas, planes y asignación de suscripciones.
   - [x] Vista en Angular `tenants-page.component.ts` para listado, métricas KPI y búsqueda.
   - [x] Modal de registro reactivo de empresas `tenant-form-modal.component.ts`.
   - [x] Modal de gestión de suscripciones y cambio de plan `subscription-modal.component.ts` con alerta de cuotas.
5. **Control de Sucursales Bajo Límites del Plan (CU04 Completado):**
   - [x] Conectar `validate_branch_quota` y `get_branch_quota` en `branch_service.py` y `branch_routes.py`.
   - [x] Endpoint `GET /api/branches/quota` y aislamiento estricto por `tenant_id`.
   - [x] Frontend `admin-branch-page.component.ts` con widget de cuota comercial del plan, barra de progreso reactiva, alerta de saturación y formulario con geolocalización.

---

### Hito 2: Persistencia Local del Catálogo (PWA e IndexedDB - CU08 & CU09)
1. **Frontend PWA:**
   - [ ] Configurar `@angular/pwa`, Service Worker y Web App Manifest.
   - [ ] Crear `src/app/core/offline/idb.service.ts` para almacenar catálogo de prendas y existencias conocidas.
   - [ ] Agregar detector de conexión (`online` / `offline`) y banner visual con advertencia de datos locales.
   - [ ] Endpoint backend `/api/catalog/offline-pack` para sincronizar lote ligero del catálogo de la empresa.

---

### Hito 3: Catálogo de Prendas y Variantes Multitenant (CU06 & CU07)
1. **Backend `p2_gestion_productos_catalogo`:**
   - [ ] CRUD de prendas y variantes de talla/precio con clave `tenant_id`.
   - [ ] Filtrado facetado por categoría, talla y rango de precio.
