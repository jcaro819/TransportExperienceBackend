# Guía de estudio del backend

Para que todo el grupo (Juan Felipe, Santiago y George) entienda el backend y pueda
defenderlo en la sustentación. Está pensada para leerse **en orden** y con el código
abierto al lado: cada paso dice qué archivo abrir y en qué fijarse.

Tiempo estimado: unas 2 horas la primera vez. Al final hay preguntas de control con sus
respuestas.

---

## Parte 0. Ponerlo a correr (20 min)

Sigue el README (sección "Puesta en marcha"). En resumen, en PowerShell:

```powershell
git clone https://github.com/jcaro819/TransportExperienceBackend.git
cd TransportExperienceBackend
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env      # y cambia JWT_SECRETO (el README dice cómo)
docker compose up -d --wait # con Docker Desktop abierto
python -m scripts.reiniciar_bd
uvicorn app.main:app --reload
```

Abre http://127.0.0.1:8000/docs. Esa página (Swagger) es la documentación viva de la API:
lista los 88 endpoints y deja probarlos. **Tenla abierta durante toda la guía.**

Usuarios de prueba, todos con la contraseña `Desarrollo2026!`:
`admin@`, `operador@`, `cliente@` y `domiciliario@transportexperience.test`.

---

## Parte 1. La idea general (10 min)

**Qué hace el sistema.** Alquila, vende y entrega a domicilio ciclas, patines y
monopatines eléctricos en Bucaramanga. Hay 4 roles: cliente, administrador, operador
(mantenimiento y entregas) y domiciliario.

**Cómo está armado.** Es un **monolito modular**: una sola aplicación, con una carpeta por
módulo dentro de `app/modulos/`:

| Carpeta | Qué hace |
|---|---|
| `usuarios` | Registro, login y gestión de usuarios y roles |
| `inventario` | Catálogo, unidades, novedades de mantenimiento, stock y alertas |
| `alquileres` | Reservas con bloqueo de 15 minutos, entrega y devolución |
| `ventas` | Compra de vehículos y accesorios (carrito) |
| `pagos` | Cobro con tarjeta o PSE por Wompi, webhook y devoluciones |
| `domicilios` | Entregas a domicilio, zonas de cobertura y estados |
| `rastreo` | Posiciones GPS de los vehículos y mapa de la flota |
| `reportes` | Actas de entrega y recepción en PDF y Excel |
| `portal` | Contenido institucional y horarios |
| `clima` | Pronóstico del clima para las fechas de un alquiler (Open-Meteo) |

**Las capas de cada módulo** (esto es lo que el profesor va a buscar):

```
petición HTTP → rutas.py → servicio.py → modelos.py → PostgreSQL
                (controlador)  (reglas de negocio)  (tablas)
```

- `rutas.py`: recibe la petición, valida la entrada, llama al servicio y arma la respuesta.
  **No tiene reglas de negocio.**
- `servicio.py`: todas las reglas ("no se puede alquilar un vehículo vendido", "máximo 30
  días"...). Aquí van la mayoría de las pruebas.
- `modelos.py`: las tablas, con SQLAlchemy.
- `esquemas.py`: qué datos entran y salen (Pydantic). Es el equivalente de los FormRequest.
- `excepciones.py`: los errores de negocio, cada uno con su código HTTP.

Mira el diagrama `docs/uml/01-paquetes.png` y luego `docs/uml/03-clases-capas.png`.

---

## Parte 2. Recorrido por los archivos base (25 min)

Ábrelos en este orden. Para cada uno: qué es y en qué fijarse.

### 2.1 `app/main.py`: el punto de entrada
Crea la aplicación y registra todos los módulos con `app.include_router(...)`.
**Fíjate en:** que cada módulo se "enchufa" aquí. Si un módulo no está aquí, sus
endpoints no existen.

### 2.2 `app/config.py`: la configuración
Lee el `.env` y lo valida al arrancar.
**Fíjate en:** el validador de `jwt_secreto`, que no deja arrancar con un secreto débil, y
en `pagos_proveedor` y `clima_proveedor`, que escogen entre el servicio real y el falso.

### 2.3 `app/db.py`: la conexión a la base
**Fíjate en:** `obtener_sesion()` y `SesionBD`. Cada petición recibe su propia sesión de
base de datos, por *inyección de dependencias* de FastAPI: la ruta solo declara
`sesion: SesionBD` y FastAPI se la entrega.

### 2.4 `app/seguridad.py`: autenticación y roles
**Fíjate en:**
- `hashear_contrasena` y `verificar_contrasena`: bcrypt; nunca se guarda la contraseña.
- `crear_token_acceso`: emite el JWT al iniciar sesión.
- `obtener_usuario_actual`: lee el token del encabezado `Authorization: Bearer ...`.
- `requiere_roles(...)` y los alias `SoloAdministrador`, `AdministradorUOperador`,
  `SoloCliente`: así se protege una ruta por rol. Es el equivalente de Gates y Policies.

**Pruébalo:** en Swagger, botón **Authorize** con el cliente, y llama `GET /usuarios` →
**403**. Ahora con el admin → **200**.

### 2.5 `app/comun/errores.py`: errores con la misma forma
Todos los errores salen así:
```json
{"error": {"codigo": "...", "mensaje": "...", "accion": "...", "detalles": null}}
```
**Fíjate en:** la clase `ErrorDeNegocio`. Cada error del sistema hereda de ella y fija su
código HTTP. El servicio lanza el error y un manejador global lo convierte en JSON: las
rutas nunca arman errores a mano.

### 2.6 `app/auditoria.py`: quién cambió qué
`registrar_auditoria(...)` guarda quién hizo un cambio sensible, cuándo y el antes y el
después. Se llama desde los servicios.

### 2.7 `alembic/versions/`: las migraciones
Cada archivo es un cambio en la estructura de la base, en orden. El primero
(`..._modelo_inicial_del_mvp.py`) crea casi todas las tablas.
**Fíjate en:** la restricción `ex_alquileres_sin_solapamiento` (busca ese nombre). Es la
que impide en la base de datos que un vehículo tenga dos alquileres con fechas cruzadas.

---

## Parte 3. Seguir una petición de punta a punta (25 min)

La mejor forma de entender el backend es seguir **una** petición completa. Usemos
**"un cliente reserva un monopatín"**: `POST /alquileres`.

**1. La ruta:** `app/modulos/alquileres/rutas.py`, función `crear`.
- `cliente: SoloCliente` → si no es cliente, responde 403 antes de entrar.
- `datos: AlquilerCrear` → Pydantic valida el cuerpo (modelo y fechas); si algo está mal,
  responde 422.
- Llama a `servicio.crear_alquiler(...)` y devuelve la respuesta.

**2. El servicio:** `app/modulos/alquileres/servicio.py`, función `crear_alquiler`. Léela
línea por línea; hace esto:
1. Valida las fechas y el máximo de días, que se lee de la base (`parametros_sistema`).
2. `_bloquear_unidades_del_modelo`: hace `SELECT ... FOR UPDATE` sobre las unidades del
   modelo. Mientras esta transacción no termine, nadie más puede reservarlas.
3. `_libres_entre`: busca una unidad libre en esas fechas.
4. Crea el `Alquiler` en estado `pendiente_pago` con `expira_en = ahora + 15 minutos`.
5. Si aun así la base rechaza el alquiler por la restricción de exclusión, responde "sin
   unidades disponibles".
6. Registra la auditoría y hace `commit`.

**3. El modelo:** `app/modulos/alquileres/modelos.py`: la tabla `alquileres` y sus estados.

**4. La prueba:** `tests/alquileres/test_concurrencia.py`. Lee
`test_dos_reservas_simultaneas_del_mismo_vehiculo_exactamente_una_gana`: lanza dos
reservas al mismo tiempo y verifica que **exactamente una gana**. Córrela:

```powershell
pytest tests/alquileres/test_concurrencia.py -v
```

**Pruébalo tú:** en Swagger, Authorize con el cliente y `POST /alquileres` con un
`modelo_id` del catálogo (`GET /catalogo/modelos`) y fechas de los próximos días.

---

## Parte 4. Las dos APIs externas (20 min)

Las dos siguen el mismo patrón: **una interfaz, una implementación real y una falsa**. El
resto del sistema solo conoce la interfaz.

### 4.1 Wompi (pagos)
- `app/modulos/pagos/pasarela.py`: la interfaz `PasarelaPagos` y `PasarelaFalsa`.
- `app/modulos/pagos/wompi.py`: `PasarelaWompi`, la que habla con Wompi por HTTP.
- `app/modulos/pagos/procesamiento.py`: `pagar(...)` hace el cobro en tres pasos:
  1. guarda el pago como `pendiente` y hace `commit`;
  2. llama a la pasarela, fuera de la transacción;
  3. aplica el resultado.
- `procesar_evento_wompi(...)`: el webhook. Verifica la **firma** del evento, descarta los
  repetidos (**idempotencia**) y guarda el cuerpo crudo.

**La idea clave:** el pago lo confirma Wompi (webhook), no el navegador del cliente.

### 4.2 Open-Meteo (clima)
Es la más sencilla; léela completa:
- `app/modulos/clima/proveedor.py`: la interfaz `ProveedorClima` y `ClimaFalso`.
- `app/modulos/clima/open_meteo.py`: `ClimaOpenMeteo`. **Es el único archivo que hace
  HTTP.**
- `app/modulos/clima/servicio.py`: `pronostico_para_alquiler(...)`, con las reglas (fechas
  válidas, días que se pueden pronosticar, aviso de lluvia).
- `app/modulos/clima/rutas.py`: `GET /clima/pronostico`.

**Pruébalo:** en Swagger, `GET /clima/pronostico` con fechas de mañana a pasado mañana.

---

## Parte 5. Las pruebas (15 min)

- `tests/conftest.py`: la preparación común.
  - Crea la base de pruebas con las mismas migraciones.
  - `sesion`: cada prueba corre en una transacción que se **revierte** al final.
  - `cliente_api`: un cliente HTTP para probar las rutas.
  - `crear_usuario` y `fabrica`: crean datos de prueba; son el equivalente de las
    Factories de Laravel.
- `tests/fabricas.py`: cómo se crean tipos, modelos, vehículos y alquileres de prueba.
- Por módulo hay `test_servicio.py` (reglas) y `test_rutas.py` (HTTP, permisos y forma de
  la respuesta).
- `tests/clima/test_open_meteo.py`: cómo se prueba una API externa **sin internet**, con
  `httpx.MockTransport`.

```powershell
pytest                 # todo (803 pruebas)
pytest tests/clima -v  # solo el clima, mostrando cada prueba
```

---

## Parte 6. Cómo repartirse el estudio

Todos leen las partes 0 a 3. Después, cada uno se vuelve "experto" en un bloque, para
responder si el profesor pregunta por él:

| Quién | Bloque | Archivos |
|---|---|---|
| Juan Felipe | Alquileres, concurrencia y pagos | `alquileres/`, `pagos/`, `tests/alquileres/test_concurrencia.py` |
| Santiago | Usuarios, seguridad, inventario y APIs externas | `app/seguridad.py`, `usuarios/`, `inventario/`, `clima/` |
| George | Ventas, domicilios, base de datos y pruebas | `ventas/`, `domicilios/`, `alembic/`, `tests/conftest.py` |

Y todos leen `docs/equivalencias-laravel.md`.

---

## Preguntas de control

Intenta responderlas antes de abrir la respuesta.

<details>
<summary>1. ¿Dónde van las reglas de negocio y por qué no en las rutas?</summary>

En `servicio.py`. Las rutas solo validan, llaman y responden. Así las reglas se prueban
sin HTTP, y la misma regla sirve desde varias rutas (por ejemplo, `poner_en_curso` se usa
al entregar en el local y al entregar un domicilio).
</details>

<details>
<summary>2. ¿Cómo se impide que dos clientes reserven el mismo vehículo al mismo tiempo?</summary>

Con dos defensas en PostgreSQL: un bloqueo de fila (`SELECT ... FOR UPDATE`) sobre las
unidades del modelo, que pone a las reservas en fila, y la restricción de exclusión
`ex_alquileres_sin_solapamiento`, que rechaza en la base dos alquileres activos del mismo
vehículo con fechas cruzadas. Un `if disponible:` en Python no sirve: dos peticiones
pueden pasar el `if` al mismo tiempo.
</details>

<details>
<summary>3. ¿Por qué las pruebas usan PostgreSQL y no SQLite?</summary>

Porque SQLite no tiene ni `FOR UPDATE` ni restricciones de exclusión. Con SQLite, las
pruebas de concurrencia pasarían sin probar nada.
</details>

<details>
<summary>4. ¿Qué pasa si una reserva no se paga en 15 minutos?</summary>

Queda vencida. Antes de crear otra reserva o compra, el servicio marca como `expirado` lo
vencido en la misma transacción (`expirar_vencidos`), y la unidad vuelve a estar libre. No
hay tareas en segundo plano.
</details>

<details>
<summary>5. ¿Cómo se protege una ruta para que solo la use el administrador?</summary>

Declarando el parámetro `administrador: SoloAdministrador` en la ruta. Es un atajo de
`requiere_roles(Rol.ADMINISTRADOR)` en `app/seguridad.py`: si el token es de otro rol,
FastAPI responde 403 antes de ejecutar la ruta.
</details>

<details>
<summary>6. ¿Por qué un cliente que pide la compra de otro recibe 404 y no 403?</summary>

Para no revelar que esa compra existe. Un 403 confirmaría que el número es válido.
</details>

<details>
<summary>7. ¿Por qué el pago no se confirma cuando el cliente vuelve a la página de éxito?</summary>

Porque el navegador se puede manipular y PSE puede tardar minutos. La verdad la da Wompi
por el webhook, que trae una firma verificable. Si el webhook no llega (en desarrollo no
puede llegar a 127.0.0.1), hay una consulta de respaldo del estado a la API de Wompi.
</details>

<details>
<summary>8. ¿Cómo se prueban Wompi y Open-Meteo sin internet?</summary>

Con las implementaciones falsas (`PasarelaFalsa`, `ClimaFalso`) y, para probar el cliente
HTTP real, con `httpx.MockTransport`, que responde como si fuera la API sin salir a la red.
</details>

<details>
<summary>9. ¿Por qué el dinero se guarda como entero?</summary>

Porque `float` tiene errores de redondeo (0.1 + 0.2 no da 0.3 exacto). En pesos
colombianos no se usan centavos, así que un entero de pesos es exacto.
</details>

<details>
<summary>10. ¿Qué es una migración y cómo se recrea la base desde cero?</summary>

Un archivo de Alembic que describe un cambio en la estructura de la base, en orden.
`python -m scripts.reiniciar_bd` quita todas las tablas, las crea de nuevo con las
migraciones y carga los datos de ejemplo: es el equivalente de
`php artisan migrate:fresh --seed`.
</details>
