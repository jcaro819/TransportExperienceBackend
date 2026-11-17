"""Cliente de Open-Meteo, la segunda API externa del sistema.

Documentación: https://open-meteo.com/en/docs. No necesita llave. Se pide el pronóstico
diario de la ciudad configurada (``CLIMA_LATITUD`` y ``CLIMA_LONGITUD``, por defecto
Bucaramanga) en hora de Colombia.

Toda la comunicación HTTP vive aquí: ni las rutas ni el servicio hablan con la API.
"""

import logging
from datetime import date
from typing import Any

import httpx

from app.config import Configuracion
from app.modulos.clima.excepciones import ClimaNoDisponible
from app.modulos.clima.proveedor import DiaClima

registro = logging.getLogger(__name__)

URL_OPEN_METEO = "https://api.open-meteo.com/v1"
# Respuesta del sistema < 3 s (SRS 3.4.1): si Open-Meteo tarda más, se avisa y ya.
_TIEMPO_ESPERA = httpx.Timeout(2.5, connect=1.5)
_VARIABLES_DIARIAS = (
    "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max"
)


class ClimaOpenMeteo:
    nombre = "open_meteo"
    dias_de_pronostico = 16

    def __init__(self, configuracion: Configuracion, cliente: httpx.Client | None = None) -> None:
        self._latitud = configuracion.clima_latitud
        self._longitud = configuracion.clima_longitud
        # ``cliente`` permite inyectar un transporte simulado en los tests.
        self._http = cliente or httpx.Client(base_url=URL_OPEN_METEO, timeout=_TIEMPO_ESPERA)

    def pronostico(self, desde: date, hasta: date) -> list[DiaClima]:
        parametros = {
            "latitude": self._latitud,
            "longitude": self._longitud,
            "daily": _VARIABLES_DIARIAS,
            "timezone": "America/Bogota",
            "start_date": desde.isoformat(),
            "end_date": hasta.isoformat(),
        }
        try:
            respuesta = self._http.get("/forecast", params=parametros)
        except httpx.HTTPError as error:
            registro.warning("Open-Meteo no respondió", extra={"error": str(error)})
            raise ClimaNoDisponible() from error
        if respuesta.status_code != 200:
            registro.warning(
                "Open-Meteo respondió con error",
                extra={"http": respuesta.status_code, "cuerpo": respuesta.text[:300]},
            )
            raise ClimaNoDisponible()
        try:
            return dias_de_respuesta(respuesta.json())
        except (KeyError, TypeError, ValueError) as error:
            registro.warning("Respuesta de Open-Meteo inesperada", extra={"error": str(error)})
            raise ClimaNoDisponible() from error


def dias_de_respuesta(cuerpo: dict[str, Any]) -> list[DiaClima]:
    """Convierte el bloque ``daily`` de Open-Meteo en ``DiaClima``.

    Open-Meteo devuelve listas paralelas (una por variable). Un valor puede venir ``null``
    si el modelo no lo tiene: se toma como 0 % de lluvia o se descarta el día si falta la
    temperatura.
    """
    diario = cuerpo["daily"]
    dias = []
    for i, fecha in enumerate(diario["time"]):
        maxima = diario["temperature_2m_max"][i]
        minima = diario["temperature_2m_min"][i]
        if maxima is None or minima is None:
            continue
        dias.append(
            DiaClima(
                fecha=date.fromisoformat(fecha),
                codigo_clima=int(diario["weather_code"][i] or 0),
                temperatura_max=float(maxima),
                temperatura_min=float(minima),
                probabilidad_lluvia=int(diario["precipitation_probability_max"][i] or 0),
            )
        )
    return dias
