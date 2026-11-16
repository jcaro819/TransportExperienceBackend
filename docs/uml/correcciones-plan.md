# Correcciones al Plan de Desarrollo de Software (documento Word, v0.3.5)

Lista de lo que hay que corregir en el Word del plan para que coincida con el código y con
sus propios números. Se revisó contra **`plan desarrollo software.docx`, versión 0.3.5**
(la del historial del 3/11/2026), que no está en el repositorio. `docs/plan-desarrollo.pdf`
es una versión anterior (v0.1.1): conviene reemplazarlo por un PDF exportado del Word cuando
estas correcciones estén aplicadas.

Las ubicaciones se dan por **número de sección** tal como lo muestra hoy el Word (y su tabla
de contenidos), no por página.

Resumen:

| # | Qué | Dónde (numeración actual del Word) |
|---|---|---|
| 1 | El nombre "TransporeExperience" | 1.4 Referencias y 4.4 Plan de Gestión de Riesgos |
| 2 | Numeración de secciones y tabla de contenidos | 1.3, 1.5, 2.3, 4.x y Anexos |
| 3 | Plan de Infraestructura vacío | 4.7 |
| 4 | Métodos, Herramientas y Técnicas, sin el stack real | 4.6 |
| 5 | "Juan Felipe Niño" en el historial de revisiones | Historial (0.3.0 y 0.3.3) y tabla del Gantt (4.3.1) |
| 6 | La tabla de esfuerzo suma 92 SP y el backlog 100 | 4.1 |
| 7 | Diagramas UML de los anexos | Anexos B a G |
| 8 | Casos de uso: UC01 a UC25 del Word → CU-01 a CU-23 | Anexos B y C |
| 9 | Otras inconsistencias encontradas al revisar | Varias |

---

## 1. "TransporeExperience" → "TransportExperience"

La portada, la introducción y las definiciones ya dicen **TransportExperience**. Quedan dos
lugares con el nombre sin la "t":

| Sección | Dice | Debe decir |
|---|---|---|
| 1.4 Referencias (primer ítem de la lista) | "Especificación de Requisitos de Software (SRS) de TransporeExperience v1.0, SystemSolutions, 2026." | "... de TransportExperience v1.0, ..." |
| 4.4 Plan de Gestión de Riesgos (párrafo inicial) | "la matriz de riesgos del proyecto TransporeExperience, identificando..." | "... del proyecto TransportExperience, ..." |

En Word: "Buscar y reemplazar" con `Transpore` para confirmar que no queda ninguno.

## 2. Numeración de secciones y tabla de contenidos

### 2.1 Lo que está mal hoy

Estructura real del Word v0.3.5 (los títulos usan numeración automática):

```
1. Introducción
   1.1 Propósito
   1.2 Alcance
   1.3 Definiciones, Acrónimos y Abreviaturas
       "A continuación se describen las definiciones clave..."   ← párrafo con estilo de título
   1.4 Referencias
   1.5 Resumen General
2. Visión General del Proyecto
   2.1 Propósito, Alcance y Objetivos del Proyecto
   2.2 Supuestos y Restricciones
   2.3 Entregables del Proyecto
       (título vacío)                                             ← párrafo vacío con estilo de título
3. Organización del Proyecto
   3.1 Estructura Organizacional
   3.2 Interfaces Externas
   3.3 Roles y Responsabilidades
4. Proceso de Gestión
   4.1 Estimaciones del Proyecto
   (4.2 no existe: lo gasta un párrafo vacío)                    ← antes de la tabla de esfuerzo
   4.3 Plan del Proyecto
       4.3.1 Plan de Fases
       4.3.2 Recursos del Proyecto
       4.3.3 Presupuesto
   4.4 Plan de Gestión de Riesgos
   (4.5 no existe: lo gasta un párrafo vacío)                    ← antes de la tabla de riesgos
   4.6 Métodos, Herramientas y Técnicas
   4.7 Plan de Infraestructura
5. Anexos
   Anexo A ... Anexo G                                            ← texto normal, no son títulos
```

| # | Problema | Dónde | Cómo se arregla en Word |
|---|---|---|---|
| a | **La numeración salta de 4.1 a 4.3.** Hay un párrafo vacío con la numeración de títulos justo antes de la tabla "Módulo / Funcionalidad" (después de la viñeta "Velocidad del Equipo..."). No se ve, pero gasta el número 4.2. | 4.1 | Poner el cursor en esa línea vacía y borrarla (o quitarle la numeración). |
| b | **Salta de 4.4 a 4.6.** Lo mismo: un párrafo vacío numerado justo antes de la tabla "Riesgo Identificado". Gasta el 4.5. | 4.4 | Borrar esa línea vacía. |
| c | La frase "A continuación se describen las definiciones clave utilizadas en este plan:" tiene estilo **Título 2**, así que sale en la tabla de contenidos como si fuera una sección. | 1.3 | Cambiarle el estilo a "Normal". |
| d | Hay un **título vacío** (estilo Título 2, sin texto) después de la lista de entregables. | Final de 2.3 | Borrarlo. |
| e | Los **anexos no aparecen en la tabla de contenidos**: "Anexo A — ...", "Anexo B — ..." hasta "Anexo G — ..." son texto normal. | 5 | Darles estilo Título 2 (sin número automático, porque ya llevan letra). |
| f | **1.5 Resumen General describe un documento que no es este**: dice que la Sección 5 "abarca los aspectos técnicos de ingeniería y herramientas UML" y que "las Secciones 6 a 9 recogen los planes de soporte, anexos e índice". El Word solo tiene 5 secciones, la 5 es Anexos, y los métodos y herramientas están en la 4. | 1.5 | Reemplazar el párrafo (texto abajo). |
| g | En el Anexo C, "UC9" está escrito sin el cero; los demás van como UC01, UC02... | Anexo C | Se resuelve al reemplazar el anexo (punto 8). |

### 2.2 Cómo debe quedar

Después de borrar los dos párrafos vacíos (a y b), Word renumera solo:

| Hoy | Debe quedar |
|---|---|
| 4.1 Estimaciones del Proyecto | 4.1 Estimaciones del Proyecto |
| 4.3 Plan del Proyecto | **4.2** Plan del Proyecto |
| 4.3.1 Plan de Fases | **4.2.1** Plan de Fases |
| 4.3.2 Recursos del Proyecto | **4.2.2** Recursos del Proyecto |
| 4.3.3 Presupuesto | **4.2.3** Presupuesto |
| 4.4 Plan de Gestión de Riesgos | **4.3** Plan de Gestión de Riesgos |
| 4.6 Métodos, Herramientas y Técnicas | **4.4** Métodos, Herramientas y Técnicas |
| 4.7 Plan de Infraestructura | **4.5** Plan de Infraestructura |
| 5. Anexos | 5. Anexos (con A a G en la tabla de contenidos) |

Al final, **actualizar la tabla de contenidos**: clic derecho sobre ella → "Actualizar
campo" → "Actualizar toda la tabla".

> En el resto de este documento las secciones se citan con su número **actual** (4.3, 4.4,
> 4.6, 4.7), para que se encuentren en el Word tal como está hoy.

Texto propuesto para **1.5 Resumen General**:

> Este documento contiene la estructura organizativa y técnica para la ejecución de
> TransportExperience. La Sección 2 ofrece una visión general con objetivos, supuestos y
> entregables. La Sección 3 detalla la estructura del equipo y sus responsabilidades. La
> Sección 4 explica el proceso de gestión: estimaciones, plan del proyecto con el Product
> Backlog y el cronograma, gestión de riesgos, métodos y herramientas, y plan de
> infraestructura. La Sección 5 reúne los anexos: la línea base COCOMO (A) y los diagramas
> UML de casos de uso, secuencia, clases, paquetes, componentes y despliegue (B a G).

## 3. Plan de Infraestructura (4.7, está vacío): texto propuesto

La sección 4.7 solo tiene el título. Texto para pegar, con lo que existe de verdad en el
repositorio:

> **Plan de Infraestructura**
>
> El MVP se ejecuta en un entorno local reproducible, idéntico para los cuatro integrantes;
> no se contrata infraestructura en la nube.
>
> **Componentes**
>
> | Componente | Tecnología | Cómo se ejecuta | Puerto |
> |---|---|---|---|
> | Frontend | HTML, CSS y JavaScript estáticos (`frontend/`: `index.html`, `app.js`, `paneles.js`, `styles.css`); mapas con Leaflet y OpenStreetMap | Servidor de archivos estáticos (`python -m http.server 5173`) | 5173 |
> | Backend (API REST) | Python 3.11+, FastAPI (`app/main.py`) | Servidor Uvicorn (`uvicorn app.main:app`) | 8000 |
> | Base de datos | PostgreSQL 16 (imagen `postgres:16-alpine`) | Contenedor `transportexperience-postgres` en Docker Compose, con el volumen `datos_postgres` | 5432 |
> | Administración de la base | Adminer (imagen `adminer`) | Contenedor `transportexperience-adminer` en Docker Compose | 8080 |
> | Simulador GPS | Python (`simulador_gps/`) | Programa aparte (`python -m simulador_gps`) que envía posiciones a la API cada 5 segundos | — |
> | Pasarela de pagos | Wompi en modo sandbox (servicio externo) | La API la consume por HTTPS; en pruebas se usa una pasarela falsa que no toca la red | 443 |
>
> **Bases de datos.** El mismo contenedor aloja la base de desarrollo
> (`transportexperience`) y la de pruebas automáticas (`transportexperience_pruebas`). El
> esquema se versiona con migraciones de Alembic (`alembic upgrade head`).
>
> **Configuración.** Todo valor que cambia entre entornos está en un archivo `.env` que no
> se sube al repositorio (plantilla en `.env.example`): credenciales de la base, secreto de
> JWT, orígenes permitidos (CORS), fuente del GPS (`GPS_FUENTE`: simulador o dispositivo) y
> proveedor de pagos (`PAGOS_PROVEEDOR`: falso o wompi). La API no arranca con llaves de
> Wompi que no sean de sandbox.
>
> **Seguridad de red.** Los puertos de PostgreSQL y Adminer se publican solo en
> `127.0.0.1`. Las contraseñas se guardan con bcrypt y las claves de los dispositivos GPS,
> como SHA-256.
>
> **Respaldo y restauración.** `python -m scripts.respaldo_bd respaldar` genera un respaldo
> con `pg_dump` dentro del contenedor, y `python -m scripts.respaldo_bd restaurar` lo
> recupera con `pg_restore` (SRS 3.3.2). El historial de posiciones GPS se conserva 7 días
> (`python -m scripts.limpiar_posiciones_gps`).
>
> **Hardware GPS.** El MVP se desarrolla y se sustenta con el simulador. Un dispositivo GPS
> real se integra sin cambiar el backend: envía sus posiciones al mismo endpoint
> (`POST /rastreo/posiciones`) con la clave de su vehículo.
>
> **Control de versiones e integración.** Repositorio Git en GitHub, una rama por historia
> de usuario y un *pull request* por rama. El diagrama de despliegue está en el Anexo G
> (`docs/uml/05-despliegue.png`).

Tres frases del plan que este texto contradice y hay que ajustar para que no choquen:

| Sección | Dice | Cambiar por |
|---|---|---|
| 2.2 Supuestos y Restricciones | "El proyecto asume la disponibilidad continua de servicios en la nube, APIs activas de pasarelas de pago y señal de seguimiento GPS." | "El proyecto asume la disponibilidad del entorno de pruebas (sandbox) de la pasarela de pagos Wompi, conexión a internet y posiciones GPS, que en el MVP provienen de un simulador." |
| 4.3.2 Recursos del Proyecto | "... licencias de desarrollo y costos de infraestructura en la nube previstos para las pruebas." | "... y la infraestructura local con Docker, sin costo: todas las herramientas son de software libre." |
| 4.3.1, Fase 4: Transición | "... despliegue y capacitación. ... imprevistos en el entorno de producción." | No hay entorno de producción en el MVP: "... despliegue local reproducible y sustentación. ... imprevistos en el entorno de demostración." |

## 4. Métodos, Herramientas y Técnicas (4.6): texto propuesto

Hoy solo dice: "Se emplearán metodologías ágiles de desarrollo, modelado formal de casos de
uso mediante UML y estándares modernos de programación web." Texto para reemplazarlo, con
el stack real (versiones mínimas de `pyproject.toml`):

> **Métodos, Herramientas y Técnicas**
>
> **Método.** Scrum, con 4 Sprints de 2 semanas. Cada historia de usuario se desarrolla en
> su propia rama y entra a `main` por *pull request*.
>
> **Arquitectura.** Monolito modular: una carpeta por módulo en `app/modulos/` (usuarios,
> inventario, alquileres, ventas, pagos, domicilios, rastreo, reportes y portal) y tres
> capas por módulo: `rutas.py` (API REST), `servicio.py` (reglas de negocio) y `modelos.py`
> (datos). `app/main.py` reúne los módulos.
>
> | Para qué | Herramienta |
> |---|---|
> | Lenguaje del backend | Python 3.11 o superior |
> | API REST y documentación OpenAPI | FastAPI, servido con Uvicorn |
> | Validación de entradas y salidas | Pydantic v2 |
> | Acceso a datos y migraciones | SQLAlchemy 2 y Alembic |
> | Base de datos | PostgreSQL 16, en Docker Compose (con Adminer) |
> | Autenticación y roles | OAuth2 con contraseña y tokens JWT (python-jose); contraseñas con bcrypt (passlib) |
> | Pasarela de pagos | Wompi en modo sandbox, consumida con httpx |
> | Documentos | ReportLab (comprobantes y actas en PDF) y openpyxl (exportación a Excel) |
> | Frontend | HTML, CSS y JavaScript, sin framework; mapas con Leaflet sobre OpenStreetMap |
> | Rastreo GPS | Simulador propio (`simulador_gps/`) que reporta por HTTP cada 5 segundos |
> | Pruebas | pytest, contra PostgreSQL real (incluye pruebas de concurrencia) |
> | Estilo y análisis de código | ruff |
> | Control de versiones | Git y GitHub |
> | Modelado | UML en PlantUML y diagrama entidad-relación en Mermaid, generados desde el código (`docs/uml/`) |
>
> **Técnicas.** Control de acceso por roles (cliente, administrador, operador y
> domiciliario); bloqueo de filas y restricción de exclusión en PostgreSQL para que un
> vehículo no se reserve dos veces; pagos confirmados por *webhook* con verificación de
> firma e idempotencia; auditoría transversal de los cambios sensibles; dinero guardado
> como enteros en pesos.

## 5. "Juan Felipe Niño" → "Juan Felipe Caro Niño"

El nombre completo es **Juan Felipe Caro Niño**, como está en 3.1, 3.3 y en la
distribución de carga de 4.3.1. En tres lugares aparece incompleto:

| Dónde | Dice | Debe decir |
|---|---|---|
| Historial de Revisiones, versión 0.3.0 (20/10/2026), columna Autor | Juan Felipe Niño | Juan Felipe Caro Niño |
| Historial de Revisiones, versión 0.3.3 (27/10/2026), columna Autor | Juan Felipe Niño | Juan Felipe Caro Niño |
| 4.3.1, tabla "Esquema del Gráfico de Gantt Conceptual", fila "Fase 2: Elaboración" | Juan Felipe Caro | Juan Felipe Caro Niño |

De paso, en el mismo historial:

- **"Julian Mejia"** (versiones 0.2.1, 0.3.1, 0.3.4 y 0.3.5) va sin tildes; en la 0.1.1 y
  en el resto del documento es **Julián Mejía**. Unificar.
- Al aplicar estas correcciones corresponde una fila nueva y subir la versión de la portada
  (hoy portada e historial coinciden en 0.3.5):

  | Fecha | Versión | Descripción | Autor |
  |---|---|---|---|
  | (fecha de la entrega) | 0.3.6 | Diagramas UML regenerados desde el código (Anexos B a G); Plan de Infraestructura; Métodos, Herramientas y Técnicas con el stack real; corrección del nombre del producto, de la numeración y de la tabla de esfuerzo. | Juan Felipe Caro Niño |

## 6. La tabla de esfuerzo suma 92 SP, no 100

La tabla "Estimación de Esfuerzo por Módulo" (4.1) suma **92 SP**, pero el Product Backlog
(4.3.1) suma **100 SP**, que es la cifra comprometida en todo el documento.

| Módulo de la tabla | SP en la tabla | Historias del backlog que lo forman |
|---|---|---|
| Portal Web Institucional | 13 | HU-01 (5) + HU-02 (8) |
| Rastreo GPS y Geolocalización | 15 | HU-08 (15) |
| Mantenimiento e Inactivación | 16 | HU-09 (8) + HU-10 (8) |
| Pasarela de Pagos Segura | 9 | HU-05 (9) |
| Gestión de Alquiler y Venta | 18 | HU-03 (10) + HU-04 (8) |
| Solicitud de Domicilios | 13 | HU-06 (8) + HU-07 (5) |
| Reportes de Entrega y Recepción | 8 | HU-11 (8) |
| **Total** | **92** | |

**Los 8 SP que faltan son HU-12** (gestión de usuarios y roles, módulo "Administración"),
que está en el backlog pero no tiene fila en la tabla de esfuerzo.

Corrección: agregar la fila y una fila de totales.

| Módulo / Funcionalidad | Horas Totales / MVP | Story Points (Calibrado) | Complejidad | Alcance MVP |
|---|---|---|---|---|
| Administración de Usuarios y Roles | (ver nota) | 8 SP | Media | Obligatorio |
| **Total** | **700 h / 350 h** | **100 SP** | | |

Nota sobre las horas: las siete filas actuales ya suman exactamente 700 h y 350 h, así que
la fila nueva necesita horas tomadas de otra. Propuesta (el equipo decide): bajar "Portal
Web Institucional" de 80 h / 40 h a 50 h / 25 h y dar 30 h / 15 h a "Administración de
Usuarios y Roles". Los totales siguen en 700 h / 350 h.

## 7. Diagramas UML de los anexos

Los diagramas de los Anexos B a G usan nombres que no existen en el código
(`AlquilerController`, `AlquilerService`, `CompraService`, `PagoController`,
`crearPublicacion()`, `finalizarAlquiler()`...). Se reemplazan por los de `docs/uml/`, que
salen del código (ver [README.md](README.md)):

| Anexo del Word | Reemplazar por |
|---|---|
| Anexo B — Diagrama de Casos de Uso | `06-casos-de-uso.png` |
| Anexo C — Diagramas de Secuencia (UC01 a UC25) | Las 23 secuencias, una por caso de uso (tabla del punto 8.4) |
| Anexo D — Diagramas de Clases | `02-clases-entidades.png` (las 21 tablas) y `03-clases-capas.png` (`rutas.py` → `servicio.py` → `modelos.py`, con `app/main.py` como control maestro) |
| Anexo E — Diagramas de Paquetes | `01-paquetes.png` |
| Anexo F — Diagramas de Componentes | `04-componentes.png` |
| Anexo G — Diagramas de Nodos | `05-despliegue.png` (en UML se llama **diagrama de despliegue**; conviene titular el anexo "Diagrama de Despliegue (nodos)") |

Si el texto del Word describe los módulos con otros nombres, usar los de las carpetas:
usuarios, inventario, alquileres, ventas, pagos, domicilios, rastreo, reportes y portal.

## 8. Casos de uso: de UC01–UC25 (Word) a CU-01–CU-23 (código)

El Anexo B del Word tiene 25 casos de uso y el Anexo C una secuencia por cada uno (UC01 a
UC25). El diagrama nuevo tiene **23 casos de uso (CU-01 a CU-23)**, que son exactamente lo
que hay en el código del MVP. No es una renumeración: unos se fusionaron, otros se quitaron
y aparecieron siete que el Word no tenía.

### 8.1 Tabla UC antiguo → CU nuevo

| UC del Word | Qué pasó | CU nuevo | Por qué |
|---|---|---|---|
| UC01 Consultar información institucional | Se mantiene | CU-01 Consultar el portal institucional y los horarios | Es `GET /portal`; incluye los horarios de atención. |
| UC02 Consultar catálogo de vehículos | Se mantiene | CU-05 Consultar el catálogo y la disponibilidad | Incluye la disponibilidad por fechas y los accesorios. |
| UC03 Solicitar alquiler de vehículo | Se mantiene | CU-09 Reservar un alquiler (bloqueo de 15 minutos) | `POST /alquileres`. |
| UC04 Consultar estado del alquiler | **Fusionado** | CU-09 | No es un flujo aparte: son las consultas `GET /alquileres/mios` y `GET /alquileres/{alquiler_id}` del mismo módulo. |
| UC05 Pagar alquiler | **Fusionado** con UC17 y UC18 | CU-13 Pagar con tarjeta o PSE y descargar el comprobante | En el código hay un solo cobro (`pagos/procesamiento.py`, `pagar()`), igual para alquileres y compras. |
| UC06 Publicar vehículo para la venta | **Fusionado** | CU-07 Gestionar el inventario y ajustar el stock | No existe una "publicación": un modelo se vende si tiene `precio_venta` y unidades disponibles. Se hace al crear o editar el modelo (`POST /inventario/modelos`, `PATCH /inventario/modelos/{modelo_id}`). |
| UC07 Comprar vehículo | Se mantiene | CU-12 Comprar vehículos y accesorios | `POST /ventas`: un carrito con vehículos y productos. |
| UC08 Gestionar inventario de vehículos | Se mantiene | CU-07 | Tipos, modelos, unidades y productos, bajo `/inventario`. |
| UC09 Solicitar domicilio (en el Word, "UC9") | Se mantiene | CU-16 Solicitar un domicilio | `POST /domicilios`. |
| UC10 Consultar estado del domicilio | Se mantiene | CU-19 Seguir el domicilio (código de rastreo) | `GET /domicilios/rastreo/{codigo}`, pública. |
| UC11 Consultar ubicación en tiempo real | Se mantiene, **cambia de actor** | CU-21 Ver el mapa de la flota y el recorrido | En el Word lo usa el cliente. En el código el mapa es solo del administrador y el operador (decisión de HU-08); el cliente ve el estado de su entrega (CU-19), no el mapa. |
| UC12 Asignar domiciliario | Se mantiene | CU-17 Asignar el domiciliario | Lo hacen el administrador o el operador, a mano. |
| UC13 Actualizar estado de entrega | Se mantiene | CU-18 Actualizar el estado de la entrega | `POST /domicilios/{domicilio_id}/estado`. |
| UC14 Confirmar entrega | **Fusionado** | CU-18 | "Entregado" es el último estado del mismo endpoint, no otro flujo. La aceptación del cliente es CU-23 (conformidad del acta). |
| UC15 Transmitir ubicación GPS | Se mantiene | CU-20 Reportar la posición GPS | `POST /rastreo/posiciones`, desde el simulador o un dispositivo. |
| UC16 Calificar servicio | **Quitado** | — | Fuera del MVP: es HU-13. No existe en el código. |
| UC17 Registrar pago de operación | **Fusionado** | CU-13 y CU-14 | No es un caso de uso (no lo inicia ningún actor): es un paso interno del cobro (`crear_cobro_pendiente()`, `registrar_resultado()`). |
| UC18 Procesar pago en línea | Se mantiene, **dividido** en dos | CU-13 y CU-14 Confirmar el pago (webhook) | El cobro lo inicia el cliente (CU-13); la confirmación la envía Wompi (CU-14). |
| UC19 Gestionar usuarios y roles | Se mantiene | CU-04 Gestionar usuarios y roles | Bajo `/usuarios`, solo el administrador. |
| UC20 Generar reportes de operaciones | Se mantiene, **acotado** | CU-22 Consultar y exportar actas (PDF y Excel) | Lo que pide HU-11 y lo que existe son las actas de entrega y recepción; no hay reportes generales de operaciones. |
| UC21 Enviar notificación automática | **Quitado** | — | Fuera del MVP: es HU-14. No hay servicio de notificaciones ni mensajería. |
| UC22 Solicitar reembolso | **Quitado** | — | No existe en el código: el cliente solo puede cancelar antes de pagar (`POST /alquileres/{alquiler_id}/cancelacion`, `POST /ventas/{venta_id}/cancelacion`). Una devolución la inicia el administrador (CU-11). |
| UC23 Procesar reembolso | Se mantiene | CU-15 Gestionar las devoluciones pendientes | El administrador hace el reembolso en el panel de Wompi y lo registra. |
| UC24 Completar alquiler de vehículo | Se mantiene, **cambia de actor** | CU-10 Entregar y recibir el vehículo en el local | En el Word lo hace el cliente. En el código la devolución la registra el administrador o el operador (`POST /alquileres/{alquiler_id}/devolucion`); el mismo caso incluye la entrega. |
| UC25 Publicación de vehículos en el catálogo ("Gestionar publicaciones activas") | **Fusionado** | CU-07 y CU-06 | No hay publicaciones: un modelo se muestra o se oculta con su campo `activo` (`PATCH /inventario/modelos/{modelo_id}`), y una unidad sale del catálogo al inactivarla (CU-06). |

Resumen: de los 25 UC, **16 se mantienen** (cuatro con cambios: UC11 y UC24 cambian de
actor, UC18 se divide y UC20 se acota), **6 se fusionan** en otros (UC04, UC05, UC06, UC14, UC17 y
UC25) y **3 se quitan** (UC16 y UC21 por estar fuera del MVP; UC22 porque no existe en el
código).

### 8.2 Casos de uso nuevos, que el Word no tenía

Existen en el código y en el backlog, pero no estaban en el Anexo B:

| CU nuevo | Historia | Por qué faltaba |
|---|---|---|
| CU-02 Editar secciones y horarios del portal | HU-01 | El Word solo tenía la consulta. El contenido es configurable por el administrador (SRS 3.5.3). |
| CU-03 Registrarse e iniciar sesión | HU-12 | El Word no tenía autenticación, aunque HU-12 exige JWT. |
| CU-06 Inactivar una unidad y gestionar novedades | HU-09 | **HU-09 no tenía ningún caso de uso** en el Word. |
| CU-08 Consultar las alertas de bajo stock | HU-10 | Criterio de aceptación de HU-10 sin caso de uso. |
| CU-11 Reasignar o cancelar con devolución | HU-03, HU-05 | Decisión del Sprint 2 para los alquileres cuya unidad entra en mantenimiento. |
| CU-14 Confirmar el pago (webhook) | HU-05 | Sale de dividir UC18: lo inicia Wompi, no el cliente. |
| CU-23 Dar conformidad a un acta | HU-11 | Es la "firma de conformidad" de HU-11. |

### 8.3 Actores

| Actor del Word | En el diagrama nuevo |
|---|---|
| Cliente, Administrador, Domiciliario | Se mantienen. |
| (no estaba) | Se agrega el **Operador**, que es un rol del sistema (mantenimiento, entregas, despacho, actas). |
| Pasarela de pagos (sistema externo) | "Wompi (sandbox)". |
| Rastreador GPS del domiciliario (dispositivo externo) | "Simulador o dispositivo GPS": la posición es de cada **vehículo**, no del domiciliario. |
| Proveedor de mapas/GPS (sistema externo) | **Se quita**: el backend no se integra con ningún proveedor de mapas. El mapa lo dibuja el frontend con Leaflet y OpenStreetMap. |
| API de notificaciones (sistema externo) | **Se quita**: HU-14 está fuera del MVP. |

También se quitan las relaciones «include» hacia "Enviar notificación automática" y los
«extend» hacia "Calificar servicio".

### 8.4 Anexo C nuevo: una secuencia por caso de uso

Reemplazar las 25 imágenes del Anexo C por estas 23 (todas en `docs/uml/`), con el título
"CU-xx Nombre" sobre cada una:

| Caso de uso | Imagen |
|---|---|
| CU-01 Consultar el portal institucional y los horarios | `12-secuencia-cu-01-consultar-portal.png` |
| CU-02 Editar secciones y horarios del portal | `13-secuencia-cu-02-editar-portal.png` |
| CU-03 Registrarse e iniciar sesión | `14-secuencia-cu-03-registro-e-inicio-de-sesion.png` |
| CU-04 Gestionar usuarios y roles | `15-secuencia-cu-04-gestionar-usuarios.png` |
| CU-05 Consultar el catálogo y la disponibilidad | `16-secuencia-cu-05-catalogo-y-disponibilidad.png` |
| CU-06 Inactivar una unidad y gestionar novedades | `17-secuencia-cu-06-inactivar-y-novedades.png` |
| CU-07 Gestionar el inventario y ajustar el stock | `18-secuencia-cu-07-gestionar-inventario.png` |
| CU-08 Consultar las alertas de bajo stock | `19-secuencia-cu-08-alertas-de-stock.png` |
| CU-09 Reservar un alquiler (bloqueo de 15 minutos) | `07-secuencia-alquiler-pago.png` |
| CU-10 Entregar y recibir el vehículo en el local | `20-secuencia-cu-10-entrega-y-recepcion.png` |
| CU-11 Reasignar o cancelar con devolución | `21-secuencia-cu-11-reasignar-o-cancelar.png` |
| CU-12 Comprar vehículos y accesorios | `08-secuencia-compra.png` |
| CU-13 Pagar con tarjeta o PSE y descargar el comprobante | `22-secuencia-cu-13-pagar-y-comprobante.png` |
| CU-14 Confirmar el pago (webhook) | `23-secuencia-cu-14-confirmar-pago-webhook.png` |
| CU-15 Gestionar las devoluciones pendientes | `24-secuencia-cu-15-devoluciones-pendientes.png` |
| CU-16 Solicitar un domicilio | `09-secuencia-domicilio.png` |
| CU-17 Asignar el domiciliario | `25-secuencia-cu-17-asignar-domiciliario.png` |
| CU-18 Actualizar el estado de la entrega | `26-secuencia-cu-18-estado-de-la-entrega.png` |
| CU-19 Seguir el domicilio (código de rastreo) | `27-secuencia-cu-19-seguir-domicilio.png` |
| CU-20 Reportar la posición GPS | `10-secuencia-posicion-gps.png` |
| CU-21 Ver el mapa de la flota y el recorrido | `28-secuencia-cu-21-mapa-de-la-flota.png` |
| CU-22 Consultar y exportar actas (PDF y Excel) | `29-secuencia-cu-22-actas-pdf-y-excel.png` |
| CU-23 Dar conformidad a un acta | `11-secuencia-conformidad-acta.png` |

Las cinco secuencias que ya existían (07 a 11) son las de CU-09, CU-12, CU-16, CU-20 y
CU-23. La 07 y la 09 muestran además el flujo completo de punta a punta (reserva, pago y
webhook; solicitud, asignación, entrega y rastreo), que las secuencias de CU-13, CU-14,
CU-17, CU-18 y CU-19 detallan por separado.

## 9. Otras inconsistencias encontradas al revisar

No estaban en la lista, pero un evaluador las va a ver:

1. **La capacidad no cuadra (4.1).** Dice que la capacidad máxima es de 140 SP y que se
   distribuye en 100 (MVP) + 10 (HU-13 y HU-14) + 40 (buffer técnico): eso suma **150**,
   no 140. O el buffer es de 30 SP, o los 10 SP opcionales salen del buffer; hay que decir
   cuál.
2. **HU-12 habla de tres roles (backlog, 4.3.1)**: "RBAC implementado (Admin, Operador,
   Cliente)". El sistema tiene cuatro: falta el **domiciliario**, que HU-06 y HU-07
   necesitan (y que el propio Anexo B dibuja como actor).
3. **HU-11 dice "firma digital de conformidad" (backlog, 4.3.1).** Lo implementado es un
   registro de conformidad (usuario, fecha y huella SHA-256 del PDF), no una firma digital
   con certificado. Ajustar la redacción del criterio, o dejar constancia de la decisión
   del equipo.
4. **Riesgo de la pasarela (tabla de 4.4)**: la mitigación habla de "arquitectura
   multi-proveedor con pasarela secundaria de respaldo (failover automático) y
   encolamiento de notificaciones de pago". Eso no existe. Lo real: pago guardado como
   pendiente antes de llamar a Wompi, *webhook* con firma e idempotencia, y consulta de
   respaldo del estado.
5. **Riesgo del GPS (tabla de 4.4)**: menciona "caché local de coordenadas" y "redundancia
   con un servicio alternativo de cartografía en la nube". Lo real: simulador GPS para no
   depender del hardware, consulta cada 5 segundos e indicador "sin señal" a los 30
   segundos.
6. **"Modo Semiaceptado" (4.1 y Anexo A)**: el modo de COCOMO 81 se llama **semiacoplado**
   (*semi-detached*).
7. **Errata (4.3.1, Fase 3)**: "APIs de terceos" → "APIs de terceros".
8. **Texto fuera de lugar (4.3.1)**: el párrafo "El cronograma del proyecto abarca un
   periodo total de 8 semanas divididas en 4 fases principales..." quedó entre la tabla
   del Product Backlog y el título "Backlog Futuro / Opcional". Va después de la tabla del
   backlog futuro, justo antes de "Dependencias entre Fases y Riesgos Asociados".
9. **Referencias (1.4)**: cita como documentos aparte un "Documento de Arquitectura de
   Software", unos "Planes de Iteración y Cronograma de Trabajo", un "Plan de Gestión de
   Riesgos del Proyecto" y unas "Guías de Modelado de Casos de Uso y UML". Si no existen,
   quitarlos o apuntar a lo que sí hay: los anexos B a G (`docs/uml/`) y las secciones 4.3
   y 4.4 del propio plan.
10. **Alcance y entregables sin HU-12 (1.2 y 2.3)**: las dos listas no mencionan la gestión
    de usuarios y roles, que sí está en el backlog (8 SP). Es la misma omisión del punto 6.
11. **Interfaces Externas (3.2)**: habla de "clientes corporativos para la validación de
    entregables". En un proyecto académico quien valida es el docente; y el proveedor de
    hardware GPS es eventual (el MVP usa el simulador).
