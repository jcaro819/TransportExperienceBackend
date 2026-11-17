"""Cliente de Open-Meteo con un transporte HTTP simulado: nunca toca internet."""

from datetime import date

import httpx
import pytest

from app.config import obtener_configuracion
from app.modulos.clima.excepciones import ClimaNoDisponible
from app.modulos.clima.open_meteo import URL_OPEN_METEO, ClimaOpenMeteo

RESPUESTA = {
    "daily": {
        "time": ["2026-11-20", "2026-11-21"],
        "weather_code": [61, 1],
        "temperature_2m_max": [26.1, 28.4],
        "temperature_2m_min": [18.0, 19.2],
        "precipitation_probability_max": [85, None],
    }
}


def _cliente(manejador) -> ClimaOpenMeteo:
    http = httpx.Client(base_url=URL_OPEN_METEO, transport=httpx.MockTransport(manejador))
    return ClimaOpenMeteo(obtener_configuracion(), cliente=http)


def test_pide_el_pronostico_diario_de_la_ciudad_y_lo_convierte():
    pedidas: list[httpx.Request] = []

    def manejador(peticion: httpx.Request) -> httpx.Response:
        pedidas.append(peticion)
        return httpx.Response(200, json=RESPUESTA)

    dias = _cliente(manejador).pronostico(date(2026, 11, 20), date(2026, 11, 21))

    parametros = pedidas[0].url.params
    assert pedidas[0].url.path == "/v1/forecast"
    assert parametros["start_date"] == "2026-11-20"
    assert parametros["end_date"] == "2026-11-21"
    assert parametros["timezone"] == "America/Bogota"
    assert "precipitation_probability_max" in parametros["daily"]
    assert [d.fecha for d in dias] == [date(2026, 11, 20), date(2026, 11, 21)]
    assert dias[0].codigo_clima == 61
    assert dias[0].probabilidad_lluvia == 85
    assert dias[1].probabilidad_lluvia == 0  # null de Open-Meteo: sin dato = 0 %


def test_un_dia_sin_temperatura_se_descarta():
    cuerpo = {"daily": {**RESPUESTA["daily"], "temperature_2m_max": [None, 28.4]}}
    dias = _cliente(lambda _: httpx.Response(200, json=cuerpo)).pronostico(
        date(2026, 11, 20), date(2026, 11, 21)
    )
    assert [d.fecha for d in dias] == [date(2026, 11, 21)]


@pytest.mark.parametrize(
    "respuesta",
    [
        httpx.Response(500, text="caído"),
        httpx.Response(400, json={"error": True, "reason": "fecha fuera de rango"}),
        httpx.Response(200, json={"sin": "daily"}),
    ],
)
def test_error_o_respuesta_inesperada_es_clima_no_disponible(respuesta):
    with pytest.raises(ClimaNoDisponible):
        _cliente(lambda _: respuesta).pronostico(date(2026, 11, 20), date(2026, 11, 20))


def test_sin_conexion_es_clima_no_disponible():
    def manejador(peticion: httpx.Request) -> httpx.Response:
        raise httpx.ConnectTimeout("sin red", request=peticion)

    with pytest.raises(ClimaNoDisponible):
        _cliente(manejador).pronostico(date(2026, 11, 20), date(2026, 11, 20))
