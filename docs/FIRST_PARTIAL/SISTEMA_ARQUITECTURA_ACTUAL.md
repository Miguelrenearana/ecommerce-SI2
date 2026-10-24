# Arquitectura Integral del Sistema (FashionStore)

**Versión:** 2.0 (Reestructuración por Paquetes de Dominio completada)  
**Fecha:** 21 de Octubre de 2026  
**Rama:** `dev-raysa`  
**Referencia Teórica:** [`docs/ARCHITECTURE_THEORY.md`](./ARCHITECTURE_THEORY.md) | [`docs/DECISION_REESTRUCTURACION_PAQUETES.md`](./DECISION_REESTRUCTURACION_PAQUETES.md)  
**Metodología de Diseño:** Principios de Módulos Profundos (*Deep Modules*) de `codebase-design` e ingeniería orientada a ICONIX / PUDS.

---

## 1. Visión General del Sistema

**FashionStore** es una plataforma omnicanal de comercio electrónico de moda y gestión de sucursales físicas que integra:
1. **Backend Transaccional y Analítico:** Construido en **FastAPI (Python)** y **PostgreSQL**, organizado en **Paquetes de Dominio Cohesivos** (P1 a P6) y preparado para la evolución a **SaaS Multitenant** (P0).
2. **Frontend Web:** Aplicación web progresiva (**Angular 21 PWA + TailwindCSS**) estructurada por perfiles de rol y flujos de cliente.
3. **Cliente Móvil:** Aplicación móvil multiplataforma (**Flutter / Dart**) orientada a la experiencia de compra, vestidor asistido y operaciones en tienda con capacidades *Offline-First*.
4. **Capa de Inteligencia Artificial Desacoplada:** Motores de filtrado colaborativo local (ALS matricial con NumPy), asistente conversacional y reportes inteligentes (Google Gemini RAG), y vestidor virtual.

```
┌────────────────────────────────────────────────────────────────────────┐
│                          CAPA DE PRESENTACIÓN                          │
│   Web (Angular 21 PWA + TailwindCSS)  │   Móvil (Flutter Android/iOS)  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTPS / REST (JSON)
┌───────────────────────────────────▼────────────────────────────────────┐
│                       BACKEND (FastAPI + Python)                       │
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │              P0: SaaS & Platform (Multitenant - Parcial 2)         │ │
│ ├────────────────────────────────────────────────────────────────────┤ │
│ │ P1: Usuarios y Acceso       │ P2: Catálogo y Productos             │ │
│ │ P3: Inventario y Stock      │ P4: Compras y Reservas               │ │
│ │ P5: Ventas y Punto de Venta │ P6: Inteligencia y Analítica         │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│         Core Transversal (Database, Config, Security, Error Handlers)  │
└──────────────┬────────────────────┬────────────────────┬───────────────┘
               │                    │                    │
┌──────────────▼─────┐   ┌──────────▼─────────┐   ┌──────▼──────────────┐
│   BASE DE DATOS    │   │  SERVICIOS DE IA   │   │ SERVICIOS EXTERNOS  │
│  PostgreSQL 15+    │   │ • Google Gemini    │   │ • Stripe Pasarela   │
│ (Transaccional,    │   │ • Decart AI / Web  │   │ • Firebase FCM      │
│  ACID, Relacional) │   │ • Motor ALS NumPy  │   │ • Cloudinary CDN    │
└────────────────────┘   └────────────────────┘   └─────────────────────┘
```

---

## 2. Arquitectura Backend (Reestructuración por Paquetes de Dominio)

### 2.1. Filosofía de Diseño (`codebase-design`: Módulos Profundos)
En lugar de una división horizontal dispersa (*Package by Layer*: `models/`, `routes/`, `schemas/`, `services/`), el backend implementa **Módulos Profundos (*Deep Modules*)**:
* **Alta Profundidad (*Depth*):** Cada paquete resuelve internamente una gran cantidad de comportamiento de negocio y persistencia compleja detrás de una interfaz pública pequeña y limpia (su `router.py`).
* **Alta Localidad (*Locality*):** Los cambios a un caso de uso específico (ej. inventario o reservas) ocurren íntegramente dentro de la carpeta del paquete correspondiente, sin esparcirse por todo el proyecto.
* **Costura Limpia (*Clean Seams*):** Cada paquete expone un enrutador consolidado hacia `main.py` (`p1_router` a `p6_router`), manteniendo desacoplado el ciclo de importaciones mediante la eliminación de dependencias circulares en los archivos `__init__.py`.
* **Compatibilidad Inversa Total (*Zero-Breakage Shims*):** Las carpetas raíz de compatibilidad (`app/models/`, `app/schemas/`, `app/services/`, `app/routes/`) reexportan transparentemente las definiciones canónicas para no romper scripts de seed, migraciones de Alembic ni pruebas unitarias existentes.

### 2.2. Mapa Canónico de Paquetes Backend

```
backend/app/
├── core/                                # Infraestructura transversal única
│   ├── config.py                        # Pydantic Settings y variables de entorno
│   ├── database.py                      # Engine SQLAlchemy, SessionLocal y Base declarativa
│   ├── security.py                      # Hashing de contraseñas y tokens JWT
│   └── error_handlers.py                # Manejadores de excepciones globales
│
├── packages/                            # Paquetes de Dominio Autónomos
│   │
│   ├── p1_gestion_usuarios_acceso/      # CU01–CU06
│   │   ├── models/                      # User, UserBodyProfile, Branch, Provider, ProviderVariantAvailability
│   │   ├── schemas/                     # user_schema, branch_schema, provider_schema, enums
│   │   ├── services/                    # user_service, branch_service, provider_service
│   │   └── routes/                      # auth, user_routes, branch_routes, provider_routes -> router.py
│   │
│   ├── p2_gestion_productos_catalogo/   # CU07–CU10
│   │   ├── models/                      # Product, ProductVariant, Category, Size, Color, Season, Collection
│   │   ├── schemas/                     # catalog_schema, garment_schema, catalog_enums
│   │   ├── services/                    # catalog_service, catalog_garment_service, cloudinary_service
│   │   └── routes/                      # catalog_routes, garment_routes -> router.py
│   │
│   ├── p3_gestion_inventario_disponibilidad/ # CU11–CU13
│   │   ├── models/                      # Inventory, InventoryMovement, ReplenishmentRequest, ReplenishmentRequestItem
│   │   ├── schemas/                     # inventory_schema, replenishment_schema
│   │   ├── services/                    # inventory_service, replenishment_service
│   │   └── routes/                      # inventory_routes, replenishment_routes -> router.py
│   │
│   ├── p4_gestion_compras_reservas/     # CU14–CU16, CU25
│   │   ├── models/                      # Cart, CartItem, Reservation, ReservationItem, Order, OrderItem, PromotionCode
│   │   ├── schemas/                     # cart_schema, reservation_schema, order_schema, payment_schema, promotion_schema
│   │   ├── services/                    # cart_service, reservation_service, order_service, pricing_service, promotion_service
│   │   └── routes/                      # cart_routes, reservation_routes, order_routes, payment_routes, promotion_routes -> router.py
│   │
│   ├── p5_gestion_ventas_pos/           # CU17–CU18
│   │   ├── models/                      # Sale, SaleItem (extensible a SaleReturn / GarmentExchange)
│   │   ├── schemas/                     # sales_schema
│   │   ├── services/                    # sales_service
│   │   └── routes/                      # sales_routes -> router.py
│   │
│   └── p6_inteligencia_analitica/       # CU19–CU24
│       ├── models/                      # Conversation, ConversationMessage, Notification, DeviceToken, CollaborativeEmbedding
│       ├── schemas/                     # chatbot_schema, dashboard_schema, notification_schema, report_schema
│       ├── services/                    # chatbot_service, conversation_service, dashboard_service, natural_report_service,
│       │                                # notification_service, notification_delivery, recommendation_service, report_service
│       └── routes/                      # chatbot_routes, dashboard_routes, notification_routes, recommendation_routes, report_routes -> router.py
│
└── main.py                              # Ensamblador maestro (96 endpoints OpenAPI verificados)
```

### 2.3. Matriz de Casos de Uso (PUDS / ICONIX) vs Paquetes Backend

| Paquete | Casos de Uso Cubiertos | Funcionalidad Principal |
|---|---|---|
| **P1** | **CU01 – CU06** | Registro de clientes, inicio de sesión JWT, CRUD de usuarios internos con RBAC, administración de sucursales físicas, gestión de cuentas y disponibilidad de proveedores, edición de perfil de usuario. |
| **P2** | **CU07 – CU10** | Catálogo general de productos, variantes por talla/color/precio, subida de imágenes a Cloudinary, categorización textil y recepción de prendas de proveedores. |
| **P3** | **CU11 – CU13** | Control de existencias por sucursal, movimientos de inventario (ingreso, egreso, traspaso entre sucursales), solicitudes de reposición y stock consolidado. |
| **P4** | **CU14 – CU16, CU25** | Gestión del carrito de compra, creación y expiración de reservas en tienda física con bloqueo de stock, órdenes online, checkout con Stripe y cupones de descuento. |
| **P5** | **CU17 – CU18** | Punto de Venta presencial (POS) para cajeros, cobro y despacho de reservas atendidas en mostrador de tienda física. |
| **P6** | **CU19 – CU24** | Recomendaciones personalizadas con ALS, Asistente Virtual Gemini (RAG con políticas y catálogo), reportes dinámicos por lenguaje natural, dashboards analíticos y notificaciones push multicanal vía FCM. |
| **P0 (Futuro)** | **Requisitos SaaS Parcial 2** | Empresas (*Tenants*), planes de suscripción, límites de cuotas y aislamiento por fila (`tenant_id`). |

---

## 3. Arquitectura Frontend Web (Angular 21 PWA)

El frontend reside en `frontend/` y está diseñado como una Progressive Web App (PWA) de alto rendimiento, optimizada con TailwindCSS y Spartan UI.

### 3.1. Estructura de Directorios (`frontend/src/app/`)
```
frontend/src/app/
├── core/                                # Capa de Infraestructura del Cliente
│   ├── guards/                          # AuthGuard, RoleGuard (RBAC por rol)
│   ├── interceptors/                    # AuthInterceptor (inyecta Authorization Bearer token)
│   ├── models/                          # Interfaces TypeScript de dominio
│   └── services/                        # ApiService, AuthService, CartStateService, NotificationService
│
├── components/                          # UI Transversal Compartida
│   ├── layout/                          # Header, Sidebar, Footer, Breadcrumbs
│   └── ui/                              # Botones, inputs, badges, diálogos modales, tablas
│
└── features/                            # Módulos Funcionales organizados por Perfil/Rol
    ├── cliente/                         # Catálogo de compras, detalle de prenda, carrito, checkout, perfil
    ├── admin/                           # Dashboard ejecutivo, gestión de usuarios, sucursales y reportes
    ├── encargado/                       # Control de stock de sucursal, confirmación de reservas, traspasos
    ├── cajero/                          # Terminal Punto de Venta (POS), atención de reservas, cobro
    ├── proveedor/                       # Portal de proveedor, abastecimiento y variantes provistas
    ├── delivery/                        # Hoja de ruta y entrega de pedidos a domicilio
    └── shared/                          # Componentes reutilizables entre vistas de rol (filtros, visores)
```

### 3.2. Principios de Integración Frontend-Backend
* **Contratos HTTP Inmutables:** Los endpoints expuestos bajo el prefijo `/api/*` se mantuvieron idénticos tras la reestructuración del backend.
* **Gestión de Estado Reactiva:** Uso de `RxJS` y Signals de Angular 21 para el carrito de compras, conteo de notificaciones y sesión del usuario.
* **Degradación Elegante:** Almacenamiento local para carritos temporales y datos de sesión mediante `localStorage`.

---

## 4. Arquitectura de la Aplicación Móvil (Flutter)

La aplicación móvil reside en `mobile/` y está desarrollada en **Flutter (Dart)** para plataformas Android e iOS.

### 4.1. Estructura Actual (`mobile/lib/`)
```
mobile/lib/
├── app/                                 # Configuración global, temas, rutas principales
├── core/                                # Red (HTTP Client / Interceptores), storage seguro, utilitarios
├── shared/                              # Widgets compartidos (Botones, campos de texto, feedback)
└── features/                            # Funcionalidades del cliente móvil
    ├── auth/                            # Inicio de sesión, registro, splash screen
    ├── catalog/                         # Exploración de prendas, filtros por temporada/color/talla
    ├── cart/                            # Carrito de compra móvil
    ├── reservations/                    # Creación y seguimiento de reservas con cuenta regresiva
    ├── orders/                          # Historial de compras y seguimiento de entregas
    ├── chatbot/                         # Asistente virtual Gemini conversacional
    ├── notifications/                   # Receptor de notificaciones push de Firebase (FCM)
    ├── profile/                         # Perfil y medidas antropométricas del cliente
    └── management/                      # Funciones operativas ligeras para personal de tienda
```

### 4.2. Propuesta de Reestructuración Móvil (`codebase-design`)
Para mantener simetría arquitectónica con el backend y preparar el proyecto para el **Modo Offline-First** y el **Examen Parcial 2**, se propone reorganizar `mobile/lib/` bajo los mismos dominios funcionales:

```
mobile/lib/
├── core/                                # Red, base de datos local (Isar/SQLite), sincronizador offline
├── modules/
│   ├── m1_identity_profile/             # Autenticación, sesión y medidas antropométricas
│   ├── m2_catalog_discovery/            # Catálogo móvil, búsqueda y previsualización de prendas
│   ├── m3_inventory_lookup/             # Disponibilidad por sucursales en tiempo real
│   ├── m4_purchases_reservations/       # Carrito, reservas con timer y checkout
│   ├── m5_pos_offline_sync/             # [PARCIAL 2] Venta rápida en tienda física con cola offline
│   └── m6_smart_assistant/              # Chatbot Gemini, recomendaciones ALS y notificaciones FCM
└── main.dart                            # Ensamblador de la aplicación móvil
```

#### Beneficios de la Propuesta Móvil:
1. **Localidad de Dominio:** Los desarrolladores reconocen los mismos paquetes tanto en el backend como en el móvil.
2. **Aislamiento Offline:** El módulo `m5_pos_offline_sync` encapsula su propia cola de sincronización de ventas (`OfflineMutationQueue`) y resolución de conflictos sin contaminar el catálogo ni el carrito.
3. **Módulos Profundos:** Cada módulo móvil expone una sola fachada de estado (`Bloc` o `Notifier`) hacia la UI, ocultando los detalles de red y base de datos local.

---

## 5. Modelo de Seguridad y Control de Acceso (RBAC + Scope)

Tanto la Web como la App Móvil se autentican mediante tokens **JWT sin estado (*Stateless*)** emitidos por el endpoint `/api/auth/login`.

### Estructura del Token JWT
```json
{
  "sub": "7a3b4c5d-0000-0000-0000-123456789abc",
  "email": "cajero.central@fashionstore.com",
  "rol": "cajero",
  "branch_id": "8f2e1a3b-1111-2222-3333-444455556666",
  "tenant_id": "00000000-0000-0000-0000-000000000001",
  "exp": 1729550000
}
```

### Reglas de Autorización por Ámbito Operativo
* **Administrador:** Acceso global a todas las sucursales, inventarios, configuraciones y reportes.
* **Encargado:** Restringido operativamente a su `branch_id`. Puede gestionar su inventario local, confirmar reservas y solicitar reposiciones a otras sucursales.
* **Cajero:** Restringido a su `branch_id`. Autorizado exclusivamente para facturar ventas en mostrador (POS) y cerrar reservas físicas.
* **Cliente:** Restringido a su `sub` (ID de usuario). Solo puede ver y alterar sus propios carritos, reservas, órdenes y perfil.
* **Proveedor:** Acceso limitado a los productos y disponibilidades asociadas a su cuenta comercial.

---

## 6. Preparación para la Expansión SaaS Multitenant (Examen Parcial 2)

La reestructuración completada deja el sistema listo para incorporar la arquitectura SaaS sin refactorizaciones traumáticas:

1. **Inyección de `p0_saas_multitenant`:** Se creará como un paquete hermano de P1 a P6 para administrar empresas (*Tenants*), planes de suscripción y límites de cuota.
2. **Contexto de Tenant Transversal:** El archivo `app/core/database.py` y `app/core/tenant_context.py` interceptará el `tenant_id` del token JWT o header HTTP para aplicar filtros automáticos a nivel de fila (*Row-Level Security / SQLAlchemy Session Filtering*).
3. **Sincronización Offline y Cambios de Prenda:** Se integrarán dentro de `p5_gestion_ventas_pos` mediante un servicio de resolución de idempotencia (`sync_service.py`) y el modelo `SaleReturn` / `GarmentExchange`.
