# Equivalencias con Laravel (Desarrollo y Arquitectura Backend)

El enunciado del proyecto final está escrito en términos de PHP y Laravel, y admite "una
tecnología similar previamente autorizada por el profesor". TransportExperience está hecho
en **Python con FastAPI**. Esta tabla dice, requisito por requisito, qué se usó en lugar de
cada pieza de Laravel y **dónde está en el repositorio**.

## Resumen

| Requisito del enunciado | Laravel | En este proyecto | Dónde |
|---|---|---|---|
| Mínimo 8 modelos y tablas | Eloquent | **19 tablas** de negocio con SQLAlchemy 2 (el ORM de Python) | `app/modulos/*/modelos.py`; diagrama en `docs/uml/modelo-datos.md` |
| Asignación masiva protegida | `$fillable` / `$guarded` | Esquemas Pydantic: cada entrada declara los campos que acepta; lo demás no llega al modelo | `app/modulos/*/esquemas.py` |
| Relaciones | `hasOne`, `hasMany`, `belongsToMany` | `relationship()` de SQLAlchemy (ver "Relaciones") | `app/modulos/*/modelos.py` |
| Migraciones | `database/migrations` | Alembic | `alembic/versions/` |
| Datos de prueba | Factories | Fábricas de objetos para las pruebas | `tests/fabricas.py`, `tests/conftest.py` |
| Seeder principal | `DatabaseSeeder.php` | Seeds idempotentes | `seeds/cargar.py`, `seeds/datos.py` |
| `migrate:fresh --seed` | Artisan | `python -m scripts.reiniciar_bd` | `scripts/reiniciar_bd.py` |
| Mínimo 4 endpoints REST | Rutas en `routes/api.php` | **88 endpoints** | `app/modulos/*/rutas.py`; contrato en `docs/api/openapi.json` |
| Códigos HTTP correctos | — | 200, 201, 400, 401, 403, 404, 409, 413, 422, 500, 503 | `app/comun/errores.py` |
| Controladores | Controllers | `rutas.py` de cada módulo: validan, llaman al servicio y arman el JSON | `app/modulos/*/rutas.py` |
| Respuestas JSON estandarizadas | API Resources | Esquemas de respuesta Pydantic y un formato único de error (`codigo`, `mensaje`, `accion`) | `app/modulos/*/esquemas.py`, `app/comun/errores.py` |
| Mínimo 2 APIs externas | — | **Wompi** (pagos con tarjeta y PSE, sandbox) y **Open-Meteo** (pronóstico del clima) | `app/modulos/pagos/wompi.py`, `app/modulos/clima/open_meteo.py` |
| Capa de servicio para lo externo | Service classes | Interfaz más implementación real más implementación falsa; nada de HTTP en rutas ni modelos | `pagos/pasarela.py` y `pagos/wompi.py`; `clima/proveedor.py` y `clima/open_meteo.py` |
| Credenciales en `.env` | `.env` y `config/services.php` | `.env` y `app/config.py` (valida todo al arrancar; rechaza llaves de Wompi que no sean de sandbox) | `.env.example`, `app/config.py` |
| Webhooks | Exención de CSRF en `VerifyCsrfToken` | `POST /pagos/webhooks/wompi` verifica la firma del evento, es idempotente y limita el cuerpo a 64 KiB. La API no usa cookies de sesión sino tokens, así que no hay CSRF que eximir | `app/modulos/pagos/rutas.py`, `pagos/procesamiento.py` |
| Registro, login y tokens | Sanctum | OAuth2 con contraseña y **JWT** (python-jose); contraseñas con bcrypt | `app/seguridad.py`, `app/modulos/usuarios/` |
| Mínimo 3 roles | — | **4 roles**: cliente, administrador, operador y domiciliario | `app/modulos/usuarios/modelos.py` (`Rol`) |
| Políticas de autorización | Gates y Policies | Dependencias por rol (`SoloAdministrador`, `AdministradorUOperador`, `SoloCliente`...) y reglas de pertenencia en los servicios (un cliente solo ve lo suyo: lo ajeno responde 404) | `app/seguridad.py` (`requiere_roles`), `app/modulos/*/servicio.py` |
| Validación de solicitudes | FormRequest | Esquemas Pydantic con restricciones y mensajes propios; un error de validación responde 422 con el detalle por campo | `app/modulos/*/esquemas.py`, `app/comun/errores.py` |
| Pruebas del 100 % de los endpoints | PHPUnit | **pytest**: los 88 endpoints tienen al menos una prueba por HTTP | `tests/` |
| Mocks de las APIs externas | `Http::fake()` | `PasarelaFalsa`, `ClimaFalso` y `httpx.MockTransport`: ninguna prueba sale a internet | `tests/pagos/test_wompi.py`, `tests/clima/` |
| Base de pruebas aislada | SQLite en memoria | PostgreSQL de pruebas separado (`transportexperience_pruebas`), creado con las mismas migraciones; cada prueba se revierte al final (ver abajo por qué no SQLite) | `tests/conftest.py` |
| Frontend que consuma el backend | Web o móvil | Web en HTML, CSS y JavaScript, con mapas en Leaflet | `frontend/` |
| README con instalación | — | Instalación, `.env.example`, migraciones, seeds y pruebas | `README.md` |

## Relaciones (uno a uno, uno a muchos, muchos a muchos)

- **Uno a muchos:** un usuario tiene muchos alquileres; un modelo de vehículo tiene muchas
  unidades; una venta tiene muchos ítems (`Venta.items`).
- **Muchos a muchos:** una venta tiene muchos vehículos y productos, y un producto aparece
  en muchas ventas. Se modela con la tabla intermedia **`items_venta`**, que además guarda
  la cantidad y el precio del momento (en Laravel sería un `belongsToMany` con pivote, o un
  modelo pivote).
- **Uno a uno:** un alquiler o una venta tiene como máximo **un domicilio vigente**. Lo
  garantiza en la base el índice único parcial `uq_domicilios_alquiler_activo` (y su par
  para ventas), no solo el código.

## Las dos APIs externas

| | Wompi | Open-Meteo |
|---|---|---|
| Para qué | Cobrar con tarjeta o PSE | Avisar si se espera lluvia en las fechas del alquiler |
| Autenticación | Llaves de sandbox en el `.env` | Ninguna (API pública) |
| Interfaz | `PasarelaPagos` | `ProveedorClima` |
| Real | `PasarelaWompi` | `ClimaOpenMeteo` |
| Falsa (pruebas) | `PasarelaFalsa` | `ClimaFalso` |
| Se escoge con | `PAGOS_PROVEEDOR=falso\|wompi` | `CLIMA_PROVEEDOR=falso\|open_meteo` |
| Endpoints | `POST /alquileres/{id}/pago`, `POST /ventas/{id}/pago`, `POST /pagos/webhooks/wompi`... | `GET /clima/pronostico` |
| Si se cae | El pago queda `pendiente` y se confirma después (webhook o consulta de respaldo) | Responde 503 con una acción clara; la reserva se puede hacer igual |

## Por qué PostgreSQL y no SQLite en las pruebas

Las dos garantías más importantes del sistema son funciones de PostgreSQL que **SQLite no
tiene**:

1. La restricción de exclusión `ex_alquileres_sin_solapamiento` (extensión `btree_gist`),
   que impide en la base que un vehículo tenga dos alquileres con fechas cruzadas.
2. El bloqueo de fila `SELECT ... FOR UPDATE`, que serializa las operaciones sobre un mismo
   vehículo.

Con SQLite, las pruebas de concurrencia (dos clientes reservando el mismo monopatín al
mismo tiempo, y que gane exactamente uno) pasarían **sin probar nada**. Por eso las pruebas
usan una base PostgreSQL separada, en el mismo contenedor de Docker, que se crea con las
mismas migraciones de Alembic que la de desarrollo. El aislamiento que pide el enunciado se
cumple: cada prueba corre dentro de una transacción que se revierte al terminar, y la base
de pruebas nunca toca la de desarrollo.

## Comandos

```powershell
docker compose up -d --wait          # PostgreSQL y Adminer
python -m scripts.reiniciar_bd       # = php artisan migrate:fresh --seed
uvicorn app.main:app --reload        # = php artisan serve   (docs en http://127.0.0.1:8000/docs)
pytest                               # = php artisan test
```
