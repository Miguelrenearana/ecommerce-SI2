# SESIÓN DE TRABAJO: IMPLEMENTACIÓN INTEGRAL CU01 (PERSISTENCIA, SEEDERS Y FRONTEND)

**Fecha:** 24 de Octubre de 2026  
**Autor:** Agente IA (Senior Architect)  
**Casos de Uso Abarcados:**
* [CU01 – Gestionar Empresas Contratantes (Tenants)](file:///c:/Users/PERSONAL/ecommerce-SI2/docs/ACTORS_AND_USE_CASES.md) [2do Parcial - NUEVO]
* [CU02 – Gestionar Planes de Suscripción y Límites Comerciales](file:///c:/Users/PERSONAL/ecommerce-SI2/docs/ACTORS_AND_USE_CASES.md) [2do Parcial - NUEVO]  
**Fase ICONIX:** Base de Datos, Persistencia Multitenant, Seeders y Frontend Web PWA (Angular 21)

---

## 1. 🎯 Objetivos de la Sesión
1. Materializar en PostgreSQL 15+ el modelo de datos multitenant para inquilinos (`companies`), planes (`plans`) y suscripciones (`subscriptions`), enlazando `tenant_id` en usuarios y sucursales.
2. Poblar la base de datos con planes oficiales (`BASICO` y `PROFESIONAL`), el Superadministrador global y dos empresas tenants independientes de prueba.
3. Desarrollar la interfaz web del Portal Master para el rol `superadmin` en Angular 21 bajo las directrices de `frontend-design` y Angular Signals.
4. Integrar el servicio reactivo con los endpoints de `/api/saas/companies` y `/api/saas/plans`, configurando la protección de rutas (`roleGuard(['superadmin'])`) y la navegación en el shell de la aplicación.

---

## 2. 🗄️ Persistencia y Base de Datos (PostgreSQL 15+)

### A. Migración Alembic `0038_add_saas_multitenant_tables.py`
* **Ejecución:** `alembic upgrade head` (Revisión: `0037` $\rightarrow$ `0038`).
* **Tabla `companies`:**
  - `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
  - `name VARCHAR(150) NOT NULL`, `business_name VARCHAR(200)`
  - `nit_rut VARCHAR(50) UNIQUE NOT NULL`, `subdomain VARCHAR(63) UNIQUE NOT NULL`
  - `email VARCHAR(120)`, `phone VARCHAR(50)`, `address TEXT`, `logo_url TEXT`
  - `status VARCHAR(20) DEFAULT 'ACTIVO' NOT NULL`
  - `created_at`, `updated_at`
* **Tabla `plans`:**
  - `id UUID PRIMARY KEY`, `name VARCHAR(100) UNIQUE`, `code VARCHAR(50) UNIQUE`
  - `description TEXT`, `price_monthly NUMERIC(10,2)`, `max_branches INT`, `has_ai_access BOOLEAN`, `is_active BOOLEAN`
* **Tabla `subscriptions`:**
  - `id UUID PRIMARY KEY`, `company_id UUID REFERENCES companies(id) ON DELETE CASCADE`
  - `plan_id UUID REFERENCES plans(id)`, `status VARCHAR(20)`, `current_period_start`, `current_period_end`
* **Modificaciones a Tablas Existentes:**
  - Clave foránea `tenant_id UUID REFERENCES companies(id)` e índices creados en `users` y `branches`.
  - Agregado el valor `'superadmin'` al tipo ENUM nativo `rolenum` en PostgreSQL.
  - Sincronización de campos de auditoría `created_at` en `users`.

### B. Seeders SaaS ([`backend/seed_saas.py`](file:///c:/Users/PERSONAL/ecommerce-SI2/backend/seed_saas.py))
* **Planes de Suscripción:**
  - `BASICO`: $29/mes, hasta 2 sucursales, sin IA generativa.
  - `PROFESIONAL`: $99/mes, hasta 10 sucursales, con módulo de IA activo.
* **Superadministrador de la Plataforma:**
  - Correo: `superadmin@fashionstore.com` | Clave: `SuperAdmin2026!` | Rol: `superadmin` | `tenant_id: None` (operador global).
* **Tenants Sembrados:**
  - **Tenant 1:** "Boutique Elegance" (Subdominio: `elegance`, NIT: `1029384756`, Plan Pro, Admin: `admin@elegance.com` / `AdminElegance2026!`, 2 sucursales operativas: Central y Equipetrol).
  - **Tenant 2:** "Moda Urbana" (Subdominio: `modaurbana`, NIT: `5647382910`, Plan Básico, Admin: `admin@modaurbana.com` / `AdminUrbana2026!`, 1 sucursal operativa: Casco Viejo).

---

## 3. 🎨 Frontend Web PWA (Angular 21)

### A. Capa de Modelos y Tipado
* [`frontend/src/app/core/models/company.model.ts`](file:///c:/Users/PERSONAL/ecommerce-SI2/frontend/src/app/core/models/company.model.ts): Tipado completo de `Company`, `Plan`, `Subscription`, `CompanyCreateDto`, `PlanType` y `CompanyStatus`.
* [`frontend/src/app/features/shared/models/auth.model.ts`](file:///c:/Users/PERSONAL/ecommerce-SI2/frontend/src/app/features/shared/models/auth.model.ts): Incorporación del rol `'superadmin'` y claim `tenant_id`.

### B. Capa de Servicios
* [`frontend/src/app/core/services/company.service.ts`](file:///c:/Users/PERSONAL/ecommerce-SI2/frontend/src/app/core/services/company.service.ts):
  - Integrado con `ApiService` para llamadas a `/api/saas/companies` y `/api/saas/plans`.
  - Métodos: `getCompanies()`, `getPlans()`, `createCompany()`, `updateCompany()`, `toggleCompanyStatus()`.

### C. Componentes UI (Portal Master Superadmin)
* [`tenant-form-modal.component.ts`](file:///c:/Users/PERSONAL/ecommerce-SI2/frontend/src/app/features/superadmin/components/tenant-form-modal.component.ts):
  - Modal accesible con `role="dialog"` y soporte para tecla `Escape`.
  - Generación automática reactiva de subdominio (*slug*) en vivo a partir de la razón social.
  - Selector visual comparativo de planes comerciales con cuotas y características destacadas.
  - Formulario reactivo con validación de campos comerciales y credenciales del administrador inicial de la empresa.
* [`tenants-page.component.ts`](file:///c:/Users/PERSONAL/ecommerce-SI2/frontend/src/app/features/superadmin/pages/tenants-page.component.ts):
  - Dashboard con métricas ejecutivas en tarjetas KPI (Total, Activas, Suspendidas).
  - Buscador reactivo por Razón Social, NIT o Subdominio.
  - Filtros tipo *pill* para estados (`all`, `ACTIVO`, `SUSPENDIDO`).
  - Tabla con información consolidada, badges y conmutador rápido de estado (Activo $\leftrightarrow$ Suspendido) con alertas Sonner toast (`toast.success`, `toast.error`).

### D. Enrutamiento y Navegación
* [`app.routes.ts`](file:///c:/Users/PERSONAL/ecommerce-SI2/frontend/src/app/app.routes.ts): Ruta `/app/superadmin/tenants` protegida con `roleGuard(['superadmin'])`.
* [`role-route.util.ts`](file:///c:/Users/PERSONAL/ecommerce-SI2/frontend/src/app/core/utils/role-route.util.ts): Redirección automática de superadmin hacia `/app/superadmin/tenants`.
* [`app-shell.component.ts`](file:///c:/Users/PERSONAL/ecommerce-SI2/frontend/src/app/core/layouts/app-shell.component.ts): Sección lateral "Plataforma SaaS Master" exclusiva para el rol `superadmin`.
* [`login-page.component.html`](file:///c:/Users/PERSONAL/ecommerce-SI2/frontend/src/app/features/shared/pages/login-page.component.html): Pestaña de acceso rápido para autenticar como Superadmin en desarrollo.

---

## 4. 🧪 Verificaciones y Pruebas
1. **PostgreSQL:** Tablas y claves foráneas verificadas; datos de prueba sembrados sin errores de integridad referencial.
2. **FastAPI OpenAPI:** Rutas `/api/saas/companies`, `/api/saas/plans` y `/api/saas/subscriptions` validadas.
3. **Angular 21 Build:** Compilación limpia mediante `ng build` (código de salida 0, sin errores de TypeScript).
