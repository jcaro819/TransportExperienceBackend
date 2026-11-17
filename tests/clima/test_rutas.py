"""GET /clima/pronostico por HTTP, con el proveedor falso (sin internet)."""

from datetime import timedelta

import pytest

from app.comun import fechas
from app.main import app
from app.modulos.clima.excepciones import ClimaNoDisponible
from app.modulos.clima.proveedor import ClimaFalso, obtener_proveedor_clima


class _ClimaCaido(ClimaFalso):
    def pronostico(self, desde, hasta):
        raise ClimaNoDisponible()


@pytest.fixture
def con_proveedor(cliente_api):
    def _usar(proveedor):
        app.dependency_overrides[obtener_proveedor_clima] = lambda: proveedor
        return cliente_api

    return _usar


def _rango(dias_desde_hoy: int, duracion: int) -> dict[str, str]:
    inicio = fechas.hoy() + timedelta(days=dias_desde_hoy)
    return {
        "fecha_inicio": inicio.isoformat(),
        "fecha_fin": (inicio + timedelta(days=duracion - 1)).isoformat(),
    }


def test_publico_y_con_aviso_si_llueve(con_proveedor):
    cliente = con_proveedor(ClimaFalso(probabilidad_lluvia=90, codigo_clima=61))

    respuesta = cliente.get("/clima/pronostico", params=_rango(1, 2))

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["fuente"] == "falso"
    assert len(cuerpo["dias"]) == 2
    assert cuerpo["dias"][0]["descripcion"] == "Lluvia"
    assert cuerpo["dias"][0]["probabilidad_lluvia"] == 90
    assert len(cuerpo["dias_con_lluvia"]) == 2
    assert cuerpo["aviso"]


def test_rango_invertido_es_422_con_error_uniforme(con_proveedor):
    cliente = con_proveedor(ClimaFalso())
    rango = _rango(3, 1)
    rango["fecha_fin"] = (fechas.hoy() + timedelta(days=1)).isoformat()

    respuesta = cliente.get("/clima/pronostico", params=rango)

    assert respuesta.status_code == 422
    assert respuesta.json()["error"]["codigo"] == "rango_de_fechas_invalido"


def test_fecha_mal_escrita_es_422(con_proveedor):
    cliente = con_proveedor(ClimaFalso())
    respuesta = cliente.get(
        "/clima/pronostico", params={"fecha_inicio": "mañana", "fecha_fin": "2026-11-20"}
    )
    assert respuesta.status_code == 422


def test_servicio_caido_es_503_con_accion(con_proveedor):
    cliente = con_proveedor(_ClimaCaido())

    respuesta = cliente.get("/clima/pronostico", params=_rango(1, 1))

    assert respuesta.status_code == 503
    error = respuesta.json()["error"]
    assert error["codigo"] == "clima_no_disponible"
    assert "reservar igual" in error["accion"]
