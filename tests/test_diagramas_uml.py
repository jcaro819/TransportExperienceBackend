"""Los diagramas de docs/uml deben decir lo mismo que el código (no necesita base de datos).

Es la red que evita que la documentación vuelva a usar nombres que no existen.
"""

import re

import pytest

from app.main import app
from scripts.generar_uml import DIR_UML, GENERADOS

# "GET /ruta" tal como se escribe en los diagramas y en el README.
_ENDPOINT = re.compile(r"\b(GET|POST|PUT|PATCH|DELETE) (/[A-Za-z0-9_{}/\-]*[A-Za-z0-9_}])")


def _endpoints_de_la_api() -> set[tuple[str, str]]:
    """Los que publica el OpenAPI: los de los módulos y ``/salud``."""
    return {
        (metodo.upper(), ruta)
        for ruta, operaciones in app.openapi()["paths"].items()
        for metodo in operaciones
    }


def _endpoints_nombrados(texto: str) -> set[tuple[str, str]]:
    return set(_ENDPOINT.findall(texto))


@pytest.mark.parametrize("nombre", sorted(GENERADOS))
def test_diagrama_generado_esta_actualizado(nombre: str) -> None:
    actual = (DIR_UML / nombre).read_text(encoding="utf-8")
    assert actual == GENERADOS[nombre](), (
        f"{nombre} está desactualizado. Ejecuta: python -m scripts.generar_uml"
    )


@pytest.mark.parametrize("archivo", sorted(p.name for p in DIR_UML.glob("*.puml")) + ["README.md"])
def test_solo_se_nombran_endpoints_que_existen(archivo: str) -> None:
    nombrados = _endpoints_nombrados((DIR_UML / archivo).read_text(encoding="utf-8"))
    inventados = sorted(nombrados - _endpoints_de_la_api())
    assert not inventados, f"{archivo} nombra endpoints que no existen en la API: {inventados}"


def test_la_trazabilidad_cubre_todos_los_endpoints() -> None:
    nombrados = _endpoints_nombrados((DIR_UML / "README.md").read_text(encoding="utf-8"))
    faltantes = sorted(_endpoints_de_la_api() - nombrados)
    assert not faltantes, f"Faltan en la tabla de docs/uml/README.md: {faltantes}"


def test_cada_diagrama_tiene_su_imagen() -> None:
    sin_imagen = sorted(
        p.name for p in DIR_UML.glob("*.puml") if not p.with_suffix(".png").exists()
    )
    assert not sin_imagen, f"Falta la PNG de: {sin_imagen}. Ejecuta: python -m scripts.generar_uml"
