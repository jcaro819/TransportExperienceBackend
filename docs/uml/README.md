# Diagramas UML de TransportExperience

Estos diagramas salen **del código**, con sus nombres reales (carpetas, archivos, clases,
funciones y endpoints, en español). Reemplazan a los del plan de desarrollo, que usaban
nombres que no existen en el repositorio.

- Formato: [PlantUML](https://plantuml.com) (`.puml`) y su imagen (`.png`) al lado, con el
  mismo nombre.
- Alcance: solo lo que existe en el MVP (HU-01 a HU-12). **HU-13 (calificaciones) y HU-14
  (alertas por SMS o correo) no están en el código**: aparecen únicamente en el diagrama de
  casos de uso, en un recuadro aparte marcado como fuera del MVP. No hay ningún servicio de
  notificaciones.

## Diagramas

| # | Diagrama | Fuente | Imagen | Cómo se mantiene |
|---|---|---|---|---|
| 1 | Paquetes: carpetas reales e importaciones | [01-paquetes.puml](01-paquetes.puml) | [png](01-paquetes.png) | Generado desde el código |
| 2 | Clases: entidades de SQLAlchemy (las 21 tablas) | [02-clases-entidades.puml](02-clases-entidades.puml) | [png](02-clases-entidades.png) | Generado desde el código |
| 3 | Clases por capas: `rutas.py` → `servicio.py` → `modelos.py` | [03-clases-capas.puml](03-clases-capas.puml) | [png](03-clases-capas.png) | Generado desde el código |
| 4 | Componentes | [04-componentes.puml](04-componentes.puml) | [png](04-componentes.png) | A mano |
| 5 | Despliegue | [05-despliegue.puml](05-despliegue.puml) | [png](05-despliegue.png) | A mano |
| 6 | Casos de uso | [06-casos-de-uso.puml](06-casos-de-uso.puml) | [png](06-casos-de-uso.png) | A mano |
| 7 | Secuencia: reservar y pagar un alquiler | [07-secuencia-alquiler-pago.puml](07-secuencia-alquiler-pago.puml) | [png](07-secuencia-alquiler-pago.png) | A mano |
| 8 | Secuencia: comprar | [08-secuencia-compra.puml](08-secuencia-compra.puml) | [png](08-secuencia-compra.png) | A mano |
| 9 | Secuencia: solicitar y seguir un domicilio | [09-secuencia-domicilio.puml](09-secuencia-domicilio.puml) | [png](09-secuencia-domicilio.png) | A mano |
| 10 | Secuencia: reportar la posición GPS | [10-secuencia-posicion-gps.puml](10-secuencia-posicion-gps.puml) | [png](10-secuencia-posicion-gps.png) | A mano |
| 11 | Secuencia: dar conformidad a un acta | [11-secuencia-conformidad-acta.puml](11-secuencia-conformidad-acta.puml) | [png](11-secuencia-conformidad-acta.png) | A mano |

### Un diagrama de secuencia por caso de uso (reemplaza el Anexo C del plan)

Cada caso de uso del MVP (CU-01 a CU-23, los del diagrama 6) tiene su secuencia, con las
rutas, las funciones y los endpoints reales. Los diagramas 7 a 11 son los flujos
principales y sirven de secuencia para su caso de uso; el 7 y el 9 recorren además el flujo
completo (pago y webhook; asignación, entrega y rastreo).

| Caso de uso | Nombre | Fuente | Imagen |
|---|---|---|---|
| CU-01 | Consultar el portal institucional y los horarios | [12-secuencia-cu-01-consultar-portal.puml](12-secuencia-cu-01-consultar-portal.puml) | [png](12-secuencia-cu-01-consultar-portal.png) |
| CU-02 | Editar secciones y horarios del portal | [13-secuencia-cu-02-editar-portal.puml](13-secuencia-cu-02-editar-portal.puml) | [png](13-secuencia-cu-02-editar-portal.png) |
| CU-03 | Registrarse e iniciar sesión | [14-secuencia-cu-03-registro-e-inicio-de-sesion.puml](14-secuencia-cu-03-registro-e-inicio-de-sesion.puml) | [png](14-secuencia-cu-03-registro-e-inicio-de-sesion.png) |
| CU-04 | Gestionar usuarios y roles | [15-secuencia-cu-04-gestionar-usuarios.puml](15-secuencia-cu-04-gestionar-usuarios.puml) | [png](15-secuencia-cu-04-gestionar-usuarios.png) |
| CU-05 | Consultar el catálogo y la disponibilidad | [16-secuencia-cu-05-catalogo-y-disponibilidad.puml](16-secuencia-cu-05-catalogo-y-disponibilidad.puml) | [png](16-secuencia-cu-05-catalogo-y-disponibilidad.png) |
| CU-06 | Inactivar una unidad y gestionar novedades | [17-secuencia-cu-06-inactivar-y-novedades.puml](17-secuencia-cu-06-inactivar-y-novedades.puml) | [png](17-secuencia-cu-06-inactivar-y-novedades.png) |
| CU-07 | Gestionar el inventario y ajustar el stock | [18-secuencia-cu-07-gestionar-inventario.puml](18-secuencia-cu-07-gestionar-inventario.puml) | [png](18-secuencia-cu-07-gestionar-inventario.png) |
| CU-08 | Consultar las alertas de bajo stock | [19-secuencia-cu-08-alertas-de-stock.puml](19-secuencia-cu-08-alertas-de-stock.puml) | [png](19-secuencia-cu-08-alertas-de-stock.png) |
| CU-09 | Reservar un alquiler (bloqueo de 15 minutos) | [07-secuencia-alquiler-pago.puml](07-secuencia-alquiler-pago.puml) | [png](07-secuencia-alquiler-pago.png) |
| CU-10 | Entregar y recibir el vehículo en el local | [20-secuencia-cu-10-entrega-y-recepcion.puml](20-secuencia-cu-10-entrega-y-recepcion.puml) | [png](20-secuencia-cu-10-entrega-y-recepcion.png) |
| CU-11 | Reasignar o cancelar con devolución | [21-secuencia-cu-11-reasignar-o-cancelar.puml](21-secuencia-cu-11-reasignar-o-cancelar.puml) | [png](21-secuencia-cu-11-reasignar-o-cancelar.png) |
| CU-12 | Comprar vehículos y accesorios | [08-secuencia-compra.puml](08-secuencia-compra.puml) | [png](08-secuencia-compra.png) |
| CU-13 | Pagar con tarjeta o PSE y descargar el comprobante | [22-secuencia-cu-13-pagar-y-comprobante.puml](22-secuencia-cu-13-pagar-y-comprobante.puml) | [png](22-secuencia-cu-13-pagar-y-comprobante.png) |
| CU-14 | Confirmar el pago (webhook) | [23-secuencia-cu-14-confirmar-pago-webhook.puml](23-secuencia-cu-14-confirmar-pago-webhook.puml) | [png](23-secuencia-cu-14-confirmar-pago-webhook.png) |
| CU-15 | Gestionar las devoluciones pendientes | [24-secuencia-cu-15-devoluciones-pendientes.puml](24-secuencia-cu-15-devoluciones-pendientes.puml) | [png](24-secuencia-cu-15-devoluciones-pendientes.png) |
| CU-16 | Solicitar un domicilio | [09-secuencia-domicilio.puml](09-secuencia-domicilio.puml) | [png](09-secuencia-domicilio.png) |
| CU-17 | Asignar el domiciliario | [25-secuencia-cu-17-asignar-domiciliario.puml](25-secuencia-cu-17-asignar-domiciliario.puml) | [png](25-secuencia-cu-17-asignar-domiciliario.png) |
| CU-18 | Actualizar el estado de la entrega | [26-secuencia-cu-18-estado-de-la-entrega.puml](26-secuencia-cu-18-estado-de-la-entrega.puml) | [png](26-secuencia-cu-18-estado-de-la-entrega.png) |
| CU-19 | Seguir el domicilio (código de rastreo) | [27-secuencia-cu-19-seguir-domicilio.puml](27-secuencia-cu-19-seguir-domicilio.puml) | [png](27-secuencia-cu-19-seguir-domicilio.png) |
| CU-20 | Reportar la posición GPS | [10-secuencia-posicion-gps.puml](10-secuencia-posicion-gps.puml) | [png](10-secuencia-posicion-gps.png) |
| CU-21 | Ver el mapa de la flota y el recorrido | [28-secuencia-cu-21-mapa-de-la-flota.puml](28-secuencia-cu-21-mapa-de-la-flota.puml) | [png](28-secuencia-cu-21-mapa-de-la-flota.png) |
| CU-22 | Consultar y exportar actas (PDF y Excel) | [29-secuencia-cu-22-actas-pdf-y-excel.puml](29-secuencia-cu-22-actas-pdf-y-excel.puml) | [png](29-secuencia-cu-22-actas-pdf-y-excel.png) |
| CU-23 | Dar conformidad a un acta | [11-secuencia-conformidad-acta.puml](11-secuencia-conformidad-acta.puml) | [png](11-secuencia-conformidad-acta.png) |

La equivalencia con los UC01 a UC25 del Word está en
[correcciones-plan.md](correcciones-plan.md).

Además: [modelo-datos.md](modelo-datos.md) (diagrama entidad-relación en Mermaid, también
generado desde los modelos) y [correcciones-plan.md](correcciones-plan.md) (lo que hay que
corregir en el documento Word del plan).

Dos aclaraciones para leerlos junto al plan:

- **El "control maestro"** es `app/main.py`: crea la aplicación FastAPI y reúne los 12
  enrutadores de los módulos (diagramas 3 y 4).
- **La "caja que comunica con el hardware"** es el módulo `app/modulos/rastreo`: recibe las
  posiciones por `POST /rastreo/posiciones`, las envíe el simulador (`simulador_gps/`) o un
  dispositivo GPS real (diagramas 4, 5 y 10).

## Cómo regenerarlos

```bash
python -m scripts.generar_uml                  # los .puml generados y todas las PNG
python -m scripts.generar_uml --sin-imagenes   # solo los .puml generados (no usa Java)
```

- Los diagramas 1, 2 y 3 se **reescriben enteros** desde el código: no se editan a mano.
- Los diagramas 4 a 29 se editan a mano; el script solo vuelve a dibujar su PNG.
- Las PNG las dibuja PlantUML, que necesita **Java** (17 o más). No hace falta Graphviz.
  El `.jar` de PlantUML no está en el repositorio: el script lo deja en `.herramientas/`
  (carpeta ignorada por git) la primera vez.
- `tests/test_diagramas_uml.py` falla si alguien cambia el código y no regenera los
  diagramas 1 a 3, si un diagrama o esta página nombran un endpoint que no existe, si un
  endpoint de la API falta en la tabla de abajo, o si a un `.puml` le falta su PNG.

## Trazabilidad: historia → código → endpoints → caso de uso → diagrama

Los casos de uso (CU) son los del diagrama 6. Todos los módulos aparecen además en los
diagramas 1 a 4. En negrita, los diagramas de secuencia.

| Historia | Carpeta del código | Endpoints | Casos de uso | Diagramas |
|---|---|---|---|---|
| **HU-01** Portal institucional | `app/modulos/portal` | `GET /portal`<br>`PUT /portal/secciones/{seccion}`<br>`PUT /portal/horarios/{dia}`<br>`DELETE /portal/horarios/{dia}` | CU-01, CU-02 | 2, 3, 6, **12**, **13** |
| **HU-02** Catálogo con filtros y disponibilidad | `app/modulos/inventario` (`rutas.py`, `servicio.py`) | `GET /catalogo/tipos`<br>`GET /catalogo/modelos`<br>`GET /catalogo/modelos/{modelo_id}`<br>`GET /catalogo/modelos/{modelo_id}/disponibilidad` | CU-05 | 2, 3, 6, **16** |
| **HU-03** Alquiler con bloqueo temporal | `app/modulos/alquileres` | `POST /alquileres`<br>`GET /alquileres/mios`<br>`GET /alquileres`<br>`GET /alquileres/{alquiler_id}`<br>`POST /alquileres/{alquiler_id}/cancelacion`<br>`POST /alquileres/{alquiler_id}/entrega`<br>`POST /alquileres/{alquiler_id}/devolucion`<br>`GET /alquileres/en-riesgo`<br>`POST /alquileres/{alquiler_id}/reasignacion` | CU-09, CU-10, CU-11 | 2, 3, 6, **7**, **20**, **21** |
| **HU-04** Compra con descuento de stock | `app/modulos/ventas` | `POST /ventas`<br>`GET /ventas/mias`<br>`GET /ventas`<br>`GET /ventas/{venta_id}`<br>`POST /ventas/{venta_id}/cancelacion`<br>`GET /ventas/{venta_id}/comprobante`<br>`GET /ventas/devoluciones-pendientes`<br>`GET /catalogo/productos` | CU-12 | 2, 3, 6, **8** |
| **HU-05** Pagos con tarjeta o PSE | `app/modulos/pagos` | `POST /alquileres/{alquiler_id}/pago`<br>`POST /ventas/{venta_id}/pago`<br>`GET /pagos/configuracion`<br>`GET /pagos/pse/bancos`<br>`POST /pagos/webhooks/wompi`<br>`GET /pagos/{referencia}`<br>`GET /pagos/{referencia}/comprobante`<br>`GET /pagos/devoluciones-pendientes`<br>`POST /pagos/{referencia}/devolucion-ejecutada`<br>`POST /alquileres/{alquiler_id}/cancelacion-con-devolucion` | CU-13, CU-14, CU-15, CU-11 | 2, 3, 4, 5, 6, **7**, **8**, **21**, **22**, **23**, **24** |
| **HU-06** Solicitud de domicilio | `app/modulos/domicilios` | `GET /domicilios/zonas`<br>`GET /domicilios/cobertura`<br>`POST /domicilios`<br>`GET /domicilios/mios`<br>`GET /domicilios`<br>`GET /domicilios/{domicilio_id}`<br>`POST /domicilios/{domicilio_id}/cancelacion`<br>`GET /domicilios/domiciliarios-disponibles`<br>`POST /domicilios/{domicilio_id}/asignacion` | CU-16, CU-17 | 2, 3, 6, **9**, **25** |
| **HU-07** Estado del domicilio y código de rastreo | `app/modulos/domicilios` | `GET /domicilios/asignados`<br>`POST /domicilios/{domicilio_id}/estado`<br>`POST /domicilios/{domicilio_id}/cancelacion-por-despacho`<br>`GET /domicilios/rastreo/{codigo}` | CU-18, CU-19 | 2, 3, 6, **9**, **26**, **27** |
| **HU-08** Rastreo GPS en mapa | `app/modulos/rastreo` y `simulador_gps/` | `POST /rastreo/posiciones`<br>`GET /rastreo/flota`<br>`GET /rastreo/vehiculos/{vehiculo_id}/recorrido`<br>`POST /rastreo/vehiculos/{vehiculo_id}/clave` | CU-20, CU-21 | 2, 3, 4, 5, 6, **10**, **28** |
| **HU-09** Inactivar unidades y novedades | `app/modulos/inventario` (`rutas.py`, `servicio.py`) | `GET /vehiculos`<br>`POST /vehiculos/{vehiculo_id}/inactivacion`<br>`GET /vehiculos/{vehiculo_id}/novedades`<br>`POST /vehiculos/{vehiculo_id}/novedades`<br>`POST /vehiculos/{vehiculo_id}/novedades/{novedad_id}/cierre` | CU-06 | 2, 3, 6, **17** |
| **HU-10** Inventario y alertas de bajo stock | `app/modulos/inventario` (`rutas_gestion.py`, `gestion.py`) | `GET /inventario/resumen`<br>`GET /inventario/alertas-stock`<br>`GET /inventario/tipos`<br>`POST /inventario/tipos`<br>`PATCH /inventario/tipos/{tipo_id}`<br>`GET /inventario/modelos`<br>`POST /inventario/modelos`<br>`PATCH /inventario/modelos/{modelo_id}`<br>`POST /inventario/unidades`<br>`PATCH /inventario/unidades/{vehiculo_id}`<br>`GET /inventario/productos`<br>`POST /inventario/productos`<br>`PATCH /inventario/productos/{producto_id}`<br>`POST /inventario/productos/{producto_id}/ajustes` | CU-07, CU-08 | 2, 3, 6, **18**, **19** |
| **HU-11** Actas de entrega y recepción | `app/modulos/reportes` | `GET /actas`<br>`GET /actas/mias`<br>`GET /actas/exportacion/excel`<br>`GET /actas/exportacion/pdf`<br>`GET /actas/{acta_id}`<br>`GET /actas/{acta_id}/pdf`<br>`POST /actas/{acta_id}/conformidad`<br>`GET /actas/{acta_id}/verificacion` | CU-22, CU-23 | 2, 3, 6, **11**, **29** |
| **HU-12** Usuarios, roles y JWT | `app/modulos/usuarios` y `app/seguridad.py` | `POST /autenticacion/token`<br>`POST /usuarios/registro`<br>`GET /usuarios/yo`<br>`GET /usuarios`<br>`POST /usuarios`<br>`GET /usuarios/{usuario_id}`<br>`PATCH /usuarios/{usuario_id}` | CU-03, CU-04 | 2, 3, 6, **14**, **15** |

Notas de la tabla:

- Las actas de HU-11 **se crean solas** al entregar o recibir un vehículo
  (`POST /alquileres/{alquiler_id}/entrega`, `POST /alquileres/{alquiler_id}/devolucion` y
  `POST /domicilios/{domicilio_id}/estado` con `entregado`); por eso no hay un endpoint
  para crearlas.
- `GET /salud` (en `app/main.py`) no pertenece a ninguna historia: es el chequeo de que la
  API y la base de datos responden.
- Transversales, sin historia propia: `app/auditoria.py` (SRS 3.5.4), `app/comun/`
  (errores, paginación, fechas), `app/db.py`, `app/config.py` y `app/parametros.py`
  (SRS 3.5.3).

## Equivalencias con lo que pide el plan

| Lo que se pidió o se decía | Qué es en el código (y en los diagramas) |
|---|---|
| "Control maestro" | `app/main.py`, que reúne los enrutadores |
| Caja que comunica con el hardware GPS | `app/modulos/rastreo` (`POST /rastreo/posiciones`), con `simulador_gps/` o un dispositivo real |
| Pasarela de pagos | Interfaz `PasarelaPagos`, con `PasarelaWompi` (sandbox) y `PasarelaFalsa` (tests y desarrollo) |
| Servicio de notificaciones ("notifications") | No existe: HU-14 está fuera del MVP |
| Calificaciones del servicio | No existe: HU-13 está fuera del MVP |
| Tres roles (HU-12: Admin, Operador, Cliente) | Cuatro actores: cliente, administrador, operador y domiciliario |
| Mantenimiento como módulo | Vive en `app/modulos/inventario` (inactivación y novedades, HU-09) |
