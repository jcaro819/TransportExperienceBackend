# Correcciones al Plan de Desarrollo de Software (documento Word)

Lista de lo que hay que corregir en el Word del plan para que coincida con el código y con
sus propios números. Se revisó contra `docs/plan-desarrollo.pdf` (13 páginas, portada
v0.1.1). Las páginas son las del PDF.

Resumen:

| # | Qué | Dónde |
|---|---|---|
| 1 | El nombre "TransporeExperience" | Portada, págs. 6 y 12 |
| 2 | Numeración de secciones y tabla de contenidos | Págs. 3-4 y 8-12 |
| 3 | Plan de Infraestructura vacío | Pág. 12 |
| 4 | Métodos, Herramientas y Técnicas, sin el stack real | Pág. 12 |
| 5 | "Juan Felipe Caro Niño" en el historial de revisiones | Págs. 2 y 11 |
| 6 | La tabla de esfuerzo suma 92 SP y el backlog 100 | Págs. 8-9 |
| 7 | Diagramas UML con nombres que no son los del código | Donde estén los diagramas |
| 8 | Otras inconsistencias encontradas al revisar | Varias |

---

## 1. "TransporeExperience" → "TransportExperience"

El nombre correcto, el que usa todo el código, es **TransportExperience** (con "t" y con la
"E" mayúscula). Aparece mal escrito, sin la "t", en tres lugares:

| Página | Dice | Debe decir |
|---|---|---|
| 1 (portada) | TransporeExperience | TransportExperience |
| 6 (1.4 Referencias) | "Especificación de Requisitos de Software (SRS) de TransporeExperience v1.0" | "... de TransportExperience v1.0" |
| 12 (Plan de Gestión de Riesgos) | "la matriz de riesgos del proyecto TransporeExperience" | "... del proyecto TransportExperience" |

Conviene usar "Buscar y reemplazar" en Word con `Transpore` para no dejar ninguno, y
revisar también el SRS, donde aparece además como "Transportexperience".

## 2. Numeración de secciones

El cuerpo del documento no sigue la numeración de su tabla de contenidos. A partir de la
4.1 todo se corre, porque dos **tablas** quedaron con número de título:

| Página | En el cuerpo dice | Qué es en realidad | Debe quedar (según la tabla de contenidos) |
|---|---|---|---|
| 8 | "4.2" delante de "Módulo / Funcionalidad" | El encabezado de la tabla de esfuerzo por módulo | Sin número: es una tabla de la 4.1 |
| 9 | 4.3 Plan del Proyecto | | 4.2 Plan del Proyecto |
| 9 | 4.3.1 Plan de Fases | | 4.2.1 Plan de Fases |
| 11 | 4.3.2 Recursos del Proyecto | | 4.2.5 Recursos del Proyecto |
| 11 | 4.3.3 Presupuesto | | 4.2.6 Presupuesto |
| 12 | 4.4 Plan de Gestión de Riesgos | | 4.5 Plan de Gestión de Riesgos |
| 12 | "4.5" delante de "Riesgo Identificado" | El encabezado de la tabla de riesgos | Sin número: es una tabla de la 4.5 |
| 12 | 4.6 Métodos, Herramientas y Técnicas | | 5.2 Métodos, Herramientas y Técnicas (dentro de "5. Planes del Proceso Técnico") |
| 12 | 4.7 Plan de Infraestructura | | 5.3 Plan de Infraestructura |
| 12 | 5. Anexos | | 8. Anexos |

Cómo arreglarlo en Word: quitar el estilo de título a las dos filas de encabezado de tabla
(déjalas como texto de tabla en negrita), revisar que cada título use el estilo "Título 1/2/3"
con numeración automática, y **actualizar la tabla de contenidos** (clic derecho →
"Actualizar campo" → "Actualizar toda la tabla").

Además, en la propia tabla de contenidos (págs. 3-4):

- Se colaron dos párrafos como si fueran títulos: "A continuación se describen las
  definiciones clave utilizadas en este plan:" (bajo 1.3) y todo el párrafo del Plan de
  Medición con sus cinco indicadores (entre 6.5 y 6.7). Tienen estilo de título por error:
  hay que pasarlos a texto normal. El párrafo de medición pertenece a la sección **4.4.6
  Plan de Medición**.
- Salta de **6.5 a 6.7**: falta la 6.6 (o la 6.7 debe ser 6.6).
- Anuncia secciones que **no existen en el cuerpo**: 4.2.2 Objetivos de la Iteración,
  4.2.3 Lanzamientos y Entregas, 4.2.4 Cronograma (su contenido está, pero sin título),
  4.3 Planes de Iteración, 4.4 Monitoreo y Control (4.4.1 a 4.4.6), 4.6 Plan de Cierre,
  5.1 Caso de Desarrollo, 5.4 Plan de Aceptación del Producto, 6. Planes del Proceso de
  Soporte (6.1 a 6.7), 7. Planes Adicionales y 9. Índice. Hay que redactarlas o quitarlas
  de la plantilla; no pueden quedar en el índice apuntando a la página 10 u 11 sin texto.
- La sección 2.4 "Evolución del Plan de Desarrollo de Software" está en el índice y tampoco
  está en el cuerpo.

## 3. Plan de Infraestructura (está vacío): texto propuesto

En la pág. 12 la sección solo tiene el título. Texto para pegar, con lo que existe de
verdad en el repositorio:

> **5.3 Plan de Infraestructura**
>
> El MVP se ejecuta en un entorno local reproducible, idéntico para los cuatro integrantes;
> no se contrata infraestructura en la nube.
>
> **Componentes**
>
> | Componente | Tecnología | Cómo se ejecuta | Puerto |
> |---|---|---|---|
> | Frontend | HTML, CSS y JavaScript estáticos (`frontend/`) | Servidor de archivos estáticos (`python -m http.server 5173`) | 5173 |
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
> de usuario y un *pull request* por rama. El diagrama de despliegue está en
> `docs/uml/05-despliegue.png`.

Dos cosas del plan que este texto contradice y hay que ajustar para que no choquen:

- **Pág. 11, "Recursos del Proyecto"**: habla de "costos de infraestructura en la nube
  previstos para las pruebas". No hay nube en el MVP: cambiar por "infraestructura local con
  Docker, sin costo".
- **Pág. 6, "Supuestos y Restricciones"**: "disponibilidad continua de servicios en la
  nube". Cambiar por la disponibilidad del sandbox de Wompi y de conexión a internet.

## 4. Métodos, Herramientas y Técnicas: texto propuesto

En la pág. 12 solo dice: "Se emplearán metodologías ágiles de desarrollo, modelado formal
de casos de uso mediante UML y estándares modernos de programación web". Texto para
reemplazarlo, con el stack real (versiones mínimas de `pyproject.toml`):

> **5.2 Métodos, Herramientas y Técnicas**
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
> | Frontend | HTML, CSS y JavaScript, sin framework |
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

## 5. "Juan Felipe Caro Niño" en el historial de revisiones

- **Pág. 2, Historial de Revisiones**: los autores que figuran son Dawer Patiño, Julián
  Mejía y "Equipo SystemSolutions / Dawer Patiño". **Juan Felipe Caro Niño no aparece**,
  aunque es integrante (págs. 7 y 11). Hay que agregarlo, con el nombre completo. Lo natural
  es una fila nueva para esta revisión:

  | Fecha | Versión | Descripción | Autor |
  |---|---|---|---|
  | (fecha de la entrega) | 0.3.0 | Diagramas UML regenerados desde el código; Plan de Infraestructura; Métodos, Herramientas y Técnicas con el stack real; corrección del nombre del producto, de la numeración y de la tabla de esfuerzo. | Juan Felipe Caro Niño |

- **Pág. 11, tabla del Gantt**: dice "Juan Felipe Caro". Debe decir **Juan Felipe Caro
  Niño**, igual que en las págs. 7 y 11.
- **Portada**: dice **v0.1.1**, pero el historial ya llega a la 0.2.0. Debe mostrar la
  última versión del historial (0.3.0 si se agrega la fila de arriba).

> Si lo que pidió el profesor sobre este nombre es otra cosa (por ejemplo, la forma de
> escribirlo), este es el punto a ajustar: en el PDF revisado el nombre no está en el
> historial.

## 6. La tabla de esfuerzo suma 92 SP, no 100

La tabla "Estimación de Esfuerzo por Módulo" (págs. 8-9) suma **92 SP**, pero el Product
Backlog (págs. 9-10) suma **100 SP**, que es la cifra comprometida en todo el documento.

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

| Módulo / Funcionalidad | Horas Totales / MVP | Story Points | Complejidad | Alcance MVP |
|---|---|---|---|---|
| Administración de Usuarios y Roles | (ver nota) | 8 SP | Media | Obligatorio |
| **Total** | **700 h / 350 h** | **100 SP** | | |

Nota sobre las horas: las siete filas actuales ya suman exactamente 700 h y 350 h, así que
la fila nueva necesita horas tomadas de otra. Propuesta (el equipo decide): bajar "Portal
Web Institucional" de 80 h / 40 h a 50 h / 25 h y dar 30 h / 15 h a "Administración de
Usuarios y Roles". Los totales siguen en 700 h / 350 h.

## 7. Diagramas UML

Reemplazar los diagramas del plan por las imágenes de `docs/uml/` (ver
[README.md](README.md)): paquetes, clases (entidades y capas), componentes, despliegue,
casos de uso y las cinco secuencias. Usan los nombres del código; no incluyen
notificaciones ni calificaciones, que están fuera del MVP.

Si el Word describe los módulos con otros nombres, usar los de las carpetas: usuarios,
inventario, alquileres, ventas, pagos, domicilios, rastreo, reportes y portal.

## 8. Otras inconsistencias encontradas al revisar

No estaban en la lista, pero un evaluador las va a ver:

1. **La capacidad no cuadra (pág. 7).** Dice que la capacidad es de 140 SP y que se
   reparte en 100 (MVP) + 10 (HU-13 y HU-14) + 40 (buffer): eso suma **150**, no 140. O el
   buffer es de 30 SP, o los 10 SP opcionales salen del buffer; hay que decir cuál.
2. **HU-12 habla de tres roles (pág. 9)**: "RBAC implementado (Admin, Operador, Cliente)".
   El sistema tiene cuatro: falta el **domiciliario**, que HU-06 y HU-07 necesitan.
3. **HU-11 dice "firma digital de conformidad" (pág. 10).** Lo implementado es un registro
   de conformidad (usuario, fecha y huella SHA-256 del PDF), no una firma digital con
   certificado. Ajustar la redacción del criterio, o dejar constancia de la decisión del
   equipo.
4. **Riesgo de la pasarela (pág. 12)**: la mitigación habla de "arquitectura multi-proveedor
   con pasarela secundaria de respaldo (failover automático) y encolamiento de
   notificaciones de pago". Eso no existe. Lo real: pago guardado como pendiente antes de
   llamar a Wompi, *webhook* con firma e idempotencia, y consulta de respaldo del estado.
5. **Riesgo del GPS (pág. 12)**: menciona "caché local de coordenadas" y "servicio
   alternativo de cartografía en la nube". Lo real: simulador GPS para no depender del
   hardware, consulta cada 5 segundos e indicador "sin señal" a los 30 segundos.
6. **"Modo Semiaceptado" (págs. 7 y 12)**: el modo de COCOMO 81 se llama **semiacoplado**
   (*semi-detached*).
7. **Erratas**: "terceos" → "terceros" (pág. 10); en la tabla de HU-13 y HU-14, "Opciona l"
   está partido (pág. 10), igual que "Probabilida d" en la tabla de riesgos (pág. 12):
   ensanchar la columna.
8. **Texto fuera de lugar (pág. 10)**: el párrafo "El cronograma del proyecto abarca un
   periodo total de 8 semanas..." quedó entre la tabla del backlog y la del backlog futuro.
   Va bajo el título 4.2.4 Cronograma del Proyecto.
9. **Referencias (pág. 6)**: cita un "Documento de Arquitectura de Software", un "Plan de
   Gestión de Riesgos del Proyecto" y unas "Guías de Modelado" como documentos aparte.
   Si no existen, quitarlos o apuntar a `docs/uml/` y a la sección de riesgos del plan.
