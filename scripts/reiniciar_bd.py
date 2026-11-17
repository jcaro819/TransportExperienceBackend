"""Borra la base de desarrollo, la recrea con las migraciones y carga los seeds.

Uso:  python -m scripts.reiniciar_bd

Es el equivalente de ``php artisan migrate:fresh --seed`` de Laravel: ``alembic downgrade
base`` (quita todas las tablas), ``alembic upgrade head`` (las crea de nuevo) y
``python -m seeds.cargar`` (usuarios de cada rol, catálogo, zonas, tarifas...).

Solo corre con ``ENTORNO=desarrollo``: **borra todos los datos** de la base del ``.env``.
"""

from pathlib import Path

from alembic import command
from alembic.config import Config

from app.config import obtener_configuracion
from seeds import cargar

RAIZ = Path(__file__).resolve().parent.parent


def main() -> None:
    configuracion = obtener_configuracion()
    if configuracion.entorno != "desarrollo":
        raise SystemExit(
            f"reiniciar_bd solo corre con ENTORNO=desarrollo (actual: '{configuracion.entorno}'): "
            "borra todos los datos."
        )
    alembic = Config(str(RAIZ / "alembic.ini"))
    alembic.set_main_option("script_location", str(RAIZ / "alembic"))
    print("1/3 Quitando todas las tablas (alembic downgrade base)...")
    command.downgrade(alembic, "base")
    print("2/3 Creando las tablas (alembic upgrade head)...")
    command.upgrade(alembic, "head")
    print("3/3 Cargando los datos de ejemplo (seeds)...")
    cargar.main()


if __name__ == "__main__":
    main()
