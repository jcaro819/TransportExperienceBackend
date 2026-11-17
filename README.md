# TransportExperience — Backend

Plataforma para alquilar, vender y entregar a domicilio ciclas, patines y monopatines
eléctricos: API REST en **Python con FastAPI**, PostgreSQL y un frontend web que la consume.

## Proyecto final — Desarrollo y Arquitectura Backend

Este repositorio es el proyecto final de la asignatura **Desarrollo y Arquitectura
Backend** (UNAB, profesor Feisar Moreno).

**Integrantes del grupo:** Juan Felipe Caro Niño, Santiago Brito y George Sebastian
Makhlouf.

**Origen y autoría.** El sistema nació como el proyecto de **Ingeniería de Software 2** del
equipo SystemSolutions ([repositorio original](https://github.com/jcaro819/Transportexperience)).
Este repositorio es una copia con todo su historial, así que cada commit conserva su autor
y su fecha. En ese equipo, Juan Felipe Caro Niño desarrolló el backend; el frontend es de
Julián Mejía y la documentación de requisitos y planeación, de Lucas Ardila y Dawer Patiño.
Lo que se agregó para esta asignatura (la segunda API externa, las pruebas que completan el
100 % de los endpoints y la equivalencia con Laravel) está en este repositorio.

**Cómo cumple el enunciado:** ver [`docs/equivalencias-laravel.md`](docs/equivalencias-laravel.md),
con cada requisito (Eloquent, Sanctum, Gates y Policies, FormRequest, `migrate:fresh
--seed`...) y dónde está su equivalente en el código.

| Requisito | Cumplimiento |
|---|---|
| Modelos y tablas (mínimo 8) | 19 tablas de negocio con SQLAlchemy 2 y migraciones de Alembic |
| Endpoints REST (mínimo 4) | 88 endpoints, documentados en OpenAPI (`/docs`) |
| APIs externas (mínimo 2) | **Wompi** (pagos, sandbox) y **Open-Meteo** (pronóstico del clima) |
| Autenticación y roles (mínimo 3) | JWT con OAuth2 y 4 roles: cliente, administrador, operador y domiciliario |
| Pruebas del 100 % de los endpoints | Los 88 endpoints tienen prueba por HTTP; APIs externas simuladas |
| Frontend | Web en `frontend/` (HTML, CSS y JavaScript) |

Más documentación:

- Requisitos: [`docs/SRS.pdf`](docs/SRS.pdf)
- Plan y backlog: [`docs/plan-desarrollo.pdf`](docs/plan-desarrollo.pdf)
- Guía de la API para el frontend: [`docs/api/README.md`](docs/api/README.md)
- Diagramas UML generados desde el código: [`docs/uml/README.md`](docs/uml/README.md)
- Abrir el sistema desde otro equipo (túnel para la sustentación): [`docs/sustentacion-tunel.md`](docs/sustentacion-tunel.md)

## Requisitos previos

- Python 3.11 o superior
- Docker Desktop (para PostgreSQL)
- Git

## Puesta en marcha

```bash
# 1. Clonar
git clone https://github.com/jcaro819/TransportExperienceBackend.git
cd TransportExperienceBackend

# 2. Crear y activar el entorno virtual (nunca instalar global)
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows (PowerShell)

# 3. Instalar dependencias del proyecto y de desarrollo
pip install -e ".[dev]"

# 4. Variables de entorno
cp .env.example .env             # Windows: copy .env.example .env
#    En el .env, cambia JWT_SECRETO por uno propio (la API no arranca con el de ejemplo):
python -c "import secrets; print(secrets.token_urlsafe(48))"

# 5. Levantar PostgreSQL y Adminer (http://localhost:8080)
docker compose up -d --wait

# 6. Crear las tablas y cargar los datos de ejemplo (= php artisan migrate:fresh --seed)
python -m scripts.reiniciar_bd   # borra la base de desarrollo y la recrea; o: alembic upgrade head

# 7. Arrancar la API
uvicorn app.main:app --reload    # docs en http://127.0.0.1:8000/docs

# 8. Correr las pruebas (en otra terminal, con el entorno activado)
pytest
```

Para ver la página: en otra terminal, `cd frontend` y `python -m http.server 5173`, y abre
http://localhost:5173.

## Datos de ejemplo (seeds)

```bash
python -m seeds.cargar     # solo con ENTORNO=desarrollo; se puede correr varias veces
```

Carga usuarios, catálogo (6 modelos, 15 unidades en estados variados), accesorios y
repuestos (3 en bajo stock), 3 zonas de cobertura aproximadas de Bucaramanga, métodos de
pago, contenido del portal (**provisional**) y horarios de atención.

Usuarios de desarrollo. **Todos tienen la contraseña `Desarrollo2026!`**. Solo existen
en bases de desarrollo: el script se niega a correr si `ENTORNO` no es `desarrollo`.

| Rol | Correo |
|---|---|
| Administrador | `admin@transportexperience.test` |
| Operador | `operador@transportexperience.test` |
| Cliente | `cliente@transportexperience.test` |
| Domiciliario | `domiciliario@transportexperience.test` |

## Respaldo y restauración (SRS 3.3.2)

El script `scripts/respaldo_bd.py` usa `pg_dump` y `pg_restore` **dentro del contenedor**
de Postgres: no hay que instalar nada más. Necesita `docker compose up -d`.

### Respaldar

```bash
python -m scripts.respaldo_bd respaldar                  # crea backups/<base>-<fecha>.dump
python -m scripts.respaldo_bd respaldar --conservar 10   # y deja solo los 10 más recientes
```

- Respalda la base de `DATABASE_URL` (la del `.env`) en el formato propio de Postgres
  (`-Fc`): comprimido y restaurable completo o por partes.
- Queda en `backups/`, que **no se sube a git**: los respaldos tienen datos personales.
- El archivo se escribe primero como `.parcial` y se renombra al terminar: nunca queda un
  respaldo a medias con apariencia de completo.
- Para respaldar a diario en Windows: Programador de tareas → "Crear tarea básica" →
  acción "Iniciar un programa": `.venv\Scripts\python.exe` con argumentos
  `-m scripts.respaldo_bd respaldar --conservar 14`, y como carpeta de inicio la del
  proyecto.

### Restaurar

**Primero, probar el respaldo sin tocar nada**, restaurándolo en otra base:

```bash
python -m scripts.respaldo_bd restaurar backups/transportexperience-2026-11-02_070509.dump --base transportexperience_prueba
```

Si la base no existe, se crea. Revísala en Adminer (http://localhost:8080) y bórrala al
terminar (`DROP DATABASE transportexperience_prueba;`).

**Para recuperar la base de trabajo** (reemplaza **todos** sus datos por los del respaldo):

1. Detén la API (Ctrl+C en la terminal de `uvicorn`), para que nadie escriba mientras tanto.
2. Restaura sobre la base del `.env`; sin `--confirmar`, el script se niega:

   ```bash
   python -m scripts.respaldo_bd restaurar backups/ARCHIVO.dump --confirmar
   ```

3. Corre `alembic upgrade head`: si el respaldo es de una versión anterior del código, lo
   pone al día.
4. Arranca la API de nuevo.

La restauración se detiene ante el primer error (`--exit-on-error`) y lo muestra.

## Comandos habituales

```bash
pytest                 # correr los tests (necesita docker compose up: usan Postgres)
ruff check .           # revisar estilo y errores
ruff format .          # formatear el código
alembic revision --autogenerate -m "descripcion"   # nueva migración
alembic upgrade head   # aplicar migraciones pendientes
python -m scripts.generar_diagrama_er   # regenerar docs/uml/modelo-datos.md
python -m scripts.generar_uml           # regenerar los diagramas UML de docs/uml (ver docs/uml/README.md)
python -m scripts.respaldo_bd respaldar   # respaldo de la base (ver arriba)
docker compose down    # apagar la base (conserva los datos)
```

## Estructura

```
app/
├── comun/          utilidades compartidas (errores, paginación, dinero)
└── modulos/
    ├── usuarios/   HU-12
    ├── inventario/ HU-02, HU-09, HU-10
    ├── alquileres/ HU-03
    ├── ventas/     HU-04
    ├── pagos/      HU-05
    ├── domicilios/ HU-06, HU-07
    ├── rastreo/    HU-08
    ├── reportes/   HU-11
    ├── portal/     HU-01
    └── clima/      segunda API externa (Open-Meteo), materia de Backend
simulador_gps/      posiciones simuladas para desarrollar HU-08 sin hardware
seeds/              datos de ejemplo
docs/uml/           diagramas (PlantUML / Mermaid)
docs/api/           OpenAPI exportado para el frontend
tests/
```

Cada módulo tendrá `modelos.py`, `esquemas.py`, `servicio.py`, `rutas.py` y
`excepciones.py`. Las reglas de negocio viven en `servicio.py`.

## Convenciones

- Commits en español referenciando la historia: `HU-03: bloqueo de vehículo al crear reserva`.
- Una rama por historia: `hu-03-alquileres`.
- El dinero se guarda como entero en pesos. Nunca `float`.
- `.env` nunca se sube al repositorio.
