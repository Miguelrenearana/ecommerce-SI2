# 📝 Bitácora de Sesión: CU04 – Gestionar Sucursales Bajo Límites del Plan
**Fecha:** 25 de Octubre de 2026  
**Responsable:** Arquitecto de Software Principal / Full-Stack Senior (FashionStore)  
**Metodología:** ICONIX (UML 2.5+)  
**Estado:** Completado y Verificado 100%

---

## 1. 🎯 Alcance y Caso de Uso Implementado
- **Código y Nombre:** `CU04: Gestionar Sucursales Bajo Límites del Plan` (Modificado del 1er Parcial / Presentación 1).
- **Requerimientos Funcionales Satisfechos:**
  - `RF-07`: CRUD completo de tiendas físicas por empresa (`tenant_id`).
  - `RF-08`: Validación estricta de límites de sucursales según plan comercial SaaS (Básico: máx. 2, Profesional: máx. 10).
- **Preparación para Hitos Posteriores:**
  - `CU21`: Incorporación de coordenadas geográficas (`latitude`, `longitude`) y dirección para trazado de rutas con OpenStreetMap en Flutter.

---

## 2. 🗄️ Cambios en Base de Datos & Migraciones Alembic
- **Migración:** [`backend/alembic/versions/0040_enrich_branches_geo_and_audit.py`](file:///c:/Users/PERSONAL/ecommerce-SI2/backend/alembic/versions/0040_enrich_branches_geo_and_audit.py) (`0039 -> 0040`).
- **Nuevas Columnas en la Tabla `branches`:**
  - `address`: `VARCHAR(255) NOT NULL DEFAULT ''`
  - `phone`: `VARCHAR(50) NOT NULL DEFAULT ''`
  - `opening_hours`: `VARCHAR(100) NOT NULL DEFAULT '09:00 - 20:00'`
  - `latitude`: `NUMERIC(10, 7) NOT NULL DEFAULT -17.7833000`
  - `longitude`: `NUMERIC(10, 7) NOT NULL DEFAULT -63.1821000`
  - `created_at`: `TIMESTAMPTZ DEFAULT now()`
  - `updated_at`: `TIMESTAMPTZ DEFAULT now()`
- **Sembrado Inicial:** Actualización de 3 sucursales sembradas en Santa Cruz y Cochabamba con coordenadas y datos reales.

---

## 3. ⚙️ Cambios en Backend (`p1_gestion_usuarios_acceso` + `p0_saas_plataforma`)
- **Modelos:**
  - [`models/branch.py`](file:///c:/Users/PERSONAL/ecommerce-SI2/backend/app/packages/p1_gestion_usuarios_acceso/models/branch.py): Mapeo SQLAlchemy ORM de las nuevas columnas y relación con `Company`.
  - Shim actualizado en [`app/models/branch.py`](file:///c:/Users/PERSONAL/ecommerce-SI2/backend/app/models/branch.py).
- **Esquemas:**
  - [`schemas/branch_schema.py`](file:///c:/Users/PERSONAL/ecommerce-SI2/backend/app/packages/p1_gestion_usuarios_acceso/schemas/branch_schema.py): Enriquecimiento de `BranchCreate`, `BranchUpdate`, `BranchRead` y creación de `BranchQuotaOut`.
  - Shim actualizado en [`app/schemas/branch_schema.py`](file:///c:/Users/PERSONAL/ecommerce-SI2/backend/app/schemas/branch_schema.py).
- **Servicios:**
  - [`services/branch_service.py`](file:///c:/Users/PERSONAL/ecommerce-SI2/backend/app/packages/p1_gestion_usuarios_acceso/services/branch_service.py):
    - `get_branch_quota(db, tenant_id)`: DTO informativo con cupos usados y disponibles.
    - `validate_branch_quota(db, tenant_id)`: Bloqueo con `ValueError` si las sucursales activas alcanzan o superan `plan.max_branches`.
    - `create_branch(db, branch, tenant_id)`: Enlace obligatorio por tenant y reseteo de default.
    - `get_branches(db, branch_id, tenant_id)`: Aislamiento multitenant estricto en lecturas.
    - `update_branch` y `set_branch_active`: Bloqueo de reactivación si el cupo está saturado.
  - Shim actualizado en [`app/services/branch_service.py`](file:///c:/Users/PERSONAL/ecommerce-SI2/backend/app/services/branch_service.py).
- **Rutas y Endpoints:**
  - [`routes/branch_routes.py`](file:///c:/Users/PERSONAL/ecommerce-SI2/backend/app/packages/p1_gestion_usuarios_acceso/routes/branch_routes.py):
    - `GET /api/branches/quota`: Reporte de cuotas para el Tenant Admin autenticado.
    - `GET /api/branches/`: Listado aislado por `tenant_id`.
    - `POST /api/branches/`: Alta con validación de cuotas (`HTTP 400` en saturación).
    - `PUT /api/branches/{id}` y `PATCH /api/branches/{id}/active`: Actualizaciones protegidas.
    - `DELETE /api/branches/{id}`: Baja segura.
  - Shim actualizado en [`app/routes/branch_routes.py`](file:///c:/Users/PERSONAL/ecommerce-SI2/backend/app/routes/branch_routes.py).

---

## 4. 🎨 Cambios en Frontend Web (Angular 21 PWA)
- **Modelos:**
  - [`admin-branch.model.ts`](file:///c:/Users/PERSONAL/ecommerce-SI2/frontend/src/app/features/admin/models/admin-branch.model.ts): Interfaces `AdminBranch`, `BranchQuota`, `CreateBranchRequest` y `UpdateBranchRequest` extendidas con geolocalización y cuotas.
- **Servicios:**
  - [`admin-branch.service.ts`](file:///c:/Users/PERSONAL/ecommerce-SI2/frontend/src/app/features/admin/services/admin-branch.service.ts): Incorporación del método `getBranchQuota()`.
- **Componente y Plantilla:**
  - [`admin-branch-page.component.ts`](file:///c:/Users/PERSONAL/ecommerce-SI2/frontend/src/app/features/admin/pages/admin-branch-page.component.ts): Carga simultánea de listado y cuotas con `quota = signal<BranchQuota | null>(null)`. Formulario reactivo ampliado con coordenadas y dirección.
  - [`admin-branch-page.component.html`](file:///c:/Users/PERSONAL/ecommerce-SI2/frontend/src/app/features/admin/pages/admin-branch-page.component.html):
    - Banner visual de cuota comercial SaaS con barra de progreso reactiva.
    - Alerta informativa en caso de capacidad máxima con recomendación de upgrade al Plan Profesional.
    - Grilla renovada con columnas de Ubicación física, Contacto/Horario y Chip de Coordenadas GPS (Lat/Lng).
    - Modal ampliado con validaciones y valores por defecto.

---

## 5. 🧪 Verificaciones y Pruebas Ejecutadas
- **Test de Lógica de Negocio:** [`scratch/test_cu04_quota_enforcement.py`](file:///C:/Users/PERSONAL/.gemini/antigravity/brain/8f34c73d-8eac-4d72-af3f-9a97aa8aa8c6/scratch/test_cu04_quota_enforcement.py)
  - `Boutique Elegance` (Plan Básico, 2 activas): Reporte 2/2 saturated, intento de 3ra sucursal bloqueado exitosamente con mensaje descriptivo.
  - `Moda Urbana` (Plan Básico, 1 activa): Creación de 2da sucursal exitosa, intento de 3ra sucursal bloqueado exitosamente. Limpieza y rollback verificados.
- **Compilación de Frontend:** `ng build` exit code 0.
- **Backend API:** FastAPI corriendo en `http://127.0.0.1:8000` con endpoints `/api/branches/quota` y `/api/branches/`.
