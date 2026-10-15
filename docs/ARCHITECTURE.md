# Arquitectura del Sistema

Documento maestro de arquitectura de software de la plataforma de comercio electrónico de moda (**FashionStore**). Define la visión tecnológica, principios rectores, organización en capas, componentes del sistema, modelo de seguridad e integración de servicios de Inteligencia Artificial.

---

## 1. Visión y Objetivos Arquitectónicos

La plataforma está diseñada como un sistema **omnicanal, modular y multi-inquilino (SaaS)** que conecta la experiencia digital (Web y Móvil) con la operación física de sucursales en tiempo real.

### Objetivos Clave
* **Omnicanalidad nativa:** Coherencia de catálogo, precios, promociones, reservas e inventario entre puntos de venta físicos (POS) y canales digitales (Web y App móvil).
* **Escalabilidad Multi-Tenant:** Capacidad de soportar múltiples marcas y cadenas comerciales de forma aislada e independiente sobre la misma infraestructura de software.
* **Resiliencia Operativa:** Continuidad operativa en sucursales físicas y dispositivos móviles ante interrupciones de conectividad a internet (Arquitectura Offline-First).
* **Integración de Inteligencia Artificial:** Incorporación de modelos de Machine Learning, Procesamiento de Lenguaje Natural, Visión por Computadora y Sistemas Expertos desacoplados del flujo transaccional crítico.

---

## 2. Principios Rectores de Diseño

* **Backend como única fuente de verdad (*Single Source of Truth*):** Las reglas de negocio, cálculos de importes, validaciones de stock y estados de órdenes residen exclusivamente en el backend.
* **Separación de Responsabilidades (*Separation of Concerns*):** Clara división entre interfaces de usuario, controladores de API, servicios de lógica de negocio y persistencia.
* **Aislamiento Multi-Tenant por Fila (*Row-Level Multi-Tenancy*):** Toda entidad de negocio está vinculada a un `tenant_id`, resuelto y filtrado automáticamente en la capa de acceso a datos.
* **Seguridad basada en Claims y RBAC:** Autenticación sin estado (*stateless*) mediante tokens JWT firmados, con autorización granular por permisos y ámbito geográfico/operativo (`branch_id`).
* **Degradación Elegante (*Graceful Fallback*):** Si un servicio externo o modelo de IA presenta latencia o caída, el sistema conmuta automáticamente a reglas determinísticas o catálogos estáticos sin interrumpir la compra.

---

## 3. Pila Tecnológica (Tech Stack)

```
┌────────────────────────────────────────────────────────────────────────┐
│                          CAPA DE PRESENTACIÓN                          │
│   Web (Angular PWA + TailwindCSS)    │    Móvil (Flutter Android/iOS)  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTPS / REST / WebSockets
┌───────────────────────────────────▼────────────────────────────────────┐
│                       CAPA DE SERVICIOS (BACKEND)                      │
│                  FastAPI (Python 3.11+) + Pydantic                     │
│         SQLAlchemy ORM  │  Alembic (Migraciones)  │  NumPy (ML)        │
└──────────────┬────────────────────┬────────────────────┬───────────────┘
               │                    │                    │
┌──────────────▼─────┐   ┌──────────▼─────────┐   ┌──────▼──────────────┐
│   BASE DE DATOS    │   │  SERVICIOS DE IA   │   │ SERVICIOS EXTERNOS  │
│  PostgreSQL 15+    │   │ • Google Gemini    │   │ • Stripe (Checkout) │
│ (Transaccional,    │   │ • Decart AI        │   │ • Firebase FCM      │
│  ACID, Relacional) │   │ • Motor ALS Local  │   │ • Cloudinary (CDN)  │
└────────────────────┘   └────────────────────┘   └─────────────────────┘
```

* **Backend Core:** FastAPI (Python), caracterizado por alto rendimiento asíncrono, tipado estricto con Pydantic y documentación OpenAPI interactiva integrada.
* **Persistencia y Datos:** PostgreSQL como motor relacional primario; SQLAlchemy para mapeo objeto-relacional y Alembic para el control de versiones del esquema de base de datos.
* **Cálculo Numérico y Machine Learning:** NumPy para operaciones matriciales optimizadas y cálculo de embeddings colaborativos.
* **Frontend Web:** Angular con TypeScript, arquitectura modular basada en componentes y soporte para Progressive Web Apps (PWA).
* **Cliente Móvil:** Flutter (Dart), compilación nativa para Android e iOS con acceso a sensores de cámara, WebViews y almacenamiento local.

---

## 4. Estructura y Capas de la Solución

El sistema implementa una **Arquitectura en Capas Limpia**:

### 4.1. Capa de Exposición (API Routers)
Controladores REST desacoplados por bounded contexts / dominios funcionales:
* `auth`: Registro, emisión y verificación de credenciales JWT.
* `users`: Gestión de perfiles de usuario, clientes y personal interno.
* `branches`: Sucursales físicas y asignación de personal.
* `catalog`: Productos, variantes, categorías, talles, colores, temporadas y colecciones.
* `inventory`: Existencias por sucursal, alertas de stock mínimo y transferencias.
* `reservations`: Reservas de prendas en tienda física con expiración temporal.
* `sales`: Registro de ventas presenciales en mostrador de caja (POS).
* `orders` & `payments`: Checkout digital, cobro con pasarela Stripe y órdenes de compra.
* `promotions` & `loyalty`: Cupones de descuento, billetera de puntos y gift cards.
* `reports` & `dashboard`: Agregaciones analíticas, exportación CSV y dashboards.
* `ai`: Endpoints de asistencia conversacional, recomendaciones y vestidor virtual.

### 4.2. Capa de Negocio (Domain Services)
Contiene la lógica y orquestación de negocio pura, aislada del protocolo de transporte (HTTP):
* Validaciones de coherencia comercial y cálculo de importes.
* Máquinas de estados finitos (estados de reservas, órdenes y solicitudes de devolución).
* Daemons y tareas asíncronas en segundo plano (liberación de stock por reservas vencidas, despacho de notificaciones push).
* Motores de inferencia lógica y algoritmos de recomendación.

### 4.3. Capa de Persistencia y Modelado de Datos
* Modelos relacionales con claves foráneas, índices compuestos y restricciones de integridad.
* Tablas transaccionales principales: `users`, `branches`, `products`, `product_variants`, `inventories`, `inventory_movements`, `reservations`, `sales`, `orders`, `promotion_codes`.
* Tablas de auditoría y movimientos: trazabilidad obligatoria para ingresos, salidas y traspasos de inventario.

---

## 5. Modelo de Identidad, Acceso y Seguridad

### 5.1. Token de Autenticación (JWT Claims)
La sesión del usuario es sin estado (*stateless*). El token JWT contiene los siguientes claims de contexto:
```json
{
  "sub": "uuid-del-usuario",
  "email": "usuario@dominio.com",
  "rol": "administrador | encargado | cajero | cliente | delivery | proveedor",
  "branch_id": "uuid-de-sucursal | null",
  "tenant_id": "uuid-de-la-organizacion"
}
```

### 5.2. Niveles de Ámbito y Autorización
1. **Ámbito Plataforma (SuperAdmin):** Acceso total a métricas globales, aprovisionamiento de tenants y planes de suscripción.
2. **Ámbito Organización (Administrador):** Control integral de una marca comercial específica (todas sus sucursales, empleados y catálogo).
3. **Ámbito Sucursal (Encargado y Cajero):** Restricción operativa al `branch_id` asignado. Solo pueden consultar y alterar stock o registrar ventas de su sucursal.
4. **Ámbito Cliente:** Acceso restringido exclusivamente a sus propios recursos (perfil, órdenes, reservas, lista de deseos y billetera personal).
5. **Ámbito Logístico (Delivery):** Visibilidad limitada a las órdenes asignadas para despacho y su hoja de ruta.

---

## 6. Arquitectura de Inteligencia Artificial

El sistema desacopla los componentes de IA en 4 estrategias según su naturaleza técnica:

1. **Modelos Predictivos en Memoria (Machine Learning Local):**
   * Algoritmo de filtrado colaborativo *Implicit Alternating Least Squares (ALS)* implementado con NumPy.
   * Entrena factores latentes en segundo plano y almacena vectores serializados en base de datos.
   * La recomendación en tiempo real se resuelve como una operación de álgebra lineal rápida (producto punto vectorial), garantizando tiempos de respuesta inferiores a 10 ms.
2. **Modelos del Lenguaje y PLN en la Nube (Google Gemini API):**
   * Procesamiento de lenguaje natural para el Asistente Virtual y conversión de comandos libres de voz a consultas estructuradas (*Text-to-SQL/Filters*).
   * Arquitectura RAG (*Retrieval-Augmented Generation*): el backend inyecta únicamente el catálogo relevante y las reglas comerciales vigentes como contexto en el prompt, mitigando alucinaciones.
3. **Visión por Computadora y Renderizado en Cliente (Decart AI / WebRTC):**
   * Acceso local a la cámara del dispositivo móvil.
   * Segmentación de silueta y estimación de pose en tiempo real, adaptando la prenda textil sobre la vista previa sin transmitir ni almacenar imágenes biométricas del cliente en el servidor.
4. **Sistemas Expertos Determinísticos:**
   * Motores de reglas de inferencia para decisiones operativas automatizadas (ej. balanceo y traspaso de stock entre sucursales) mediante evaluación lógica de umbrales y rotación.

---

## 7. Estrategia de Resiliencia y Modo Offline

Para garantizar la continuidad operativa en locales comerciales y movilidad:

* **Aplicación Web (PWA):**
  * Service Workers que interceptan solicitudes de red y gestionan estrategias de caché (*Cache-First* para assets estáticos y recursos del catálogo; *Network-First* con fallback a caché para datos dinámicos).
  * Web App Manifest para permitir instalación en escritorios y dispositivos móviles.
* **Aplicación Móvil (Flutter Offline-First):**
  * Base de datos local embebida en el dispositivo móvil para almacenamiento de credenciales, catálogo sincronizado y compras locales.
  * Cola de mutaciones pendientes (*Offline Queue*): las ventas o transacciones realizadas sin conexión se persisten localmente con clave de idempotencia y se sincronizan atómicamente con el backend en cuanto se reanuda la conectividad.

---

## 8. Comunicación e Integraciones Asíncronas

* **Notificaciones Push en Tiempo Real:** Integración con Google Firebase Cloud Messaging (FCM) a través de un servicio desacoplado de backend. Los eventos de dominio (actualización de orden, preparación de reserva, alerta de inventario) disparan mensajes push que no bloquean la respuesta HTTP principal.
* **Webhooks Transaccionales:** Recepción asíncrona de eventos de pasarela de pago (Stripe) con validación criptográfica de firmas para confirmar pagos de checkout o eventos de renovación/cancelación de suscripciones B2B.
