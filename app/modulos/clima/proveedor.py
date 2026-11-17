"""Interfaz con el servicio del clima y su implementación falsa.

El servicio (``servicio.py``) solo conoce ``ProveedorClima``. Hay dos implementaciones:

- ``ClimaFalso``: no toca la red. Para tests y para trabajar sin internet.
- ``ClimaOpenMeteo`` (``open_meteo.py``): la API real. Se escoge con
  ``CLIMA_PROVEEDOR=open_meteo``.
"""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Protocol

from app.config import obtener_configuracion


@dataclass(frozen=True)
class DiaClima:
    """El pronóstico de un día, como lo entrega el proveedor."""

    fecha: date
    codigo_clima: int  # código WMO (0 = despejado, 61 = lluvia...)
    temperatura_max: float  # °C
    temperatura_min: float  # °C
    probabilidad_lluvia: int  # %, 0 a 100


class ProveedorClima(Protocol):
    nombre: str
    # Días hacia adelante que el proveedor puede pronosticar (Open-Meteo: 16).
    dias_de_pronostico: int

    def pronostico(self, desde: date, hasta: date) -> list[DiaClima]:
        """Pronóstico diario de ``desde`` a ``hasta``, ambos inclusive.

        Lanza ``ClimaNoDisponible`` si el servicio no responde.
        """
        ...


class ClimaFalso:
    """Proveedor de mentiras para tests y desarrollo sin internet.

    Responde el mismo día para todas las fechas: ``probabilidad_lluvia`` y
    ``codigo_clima`` se pueden fijar al crearlo. ``consultas`` guarda lo que se le pidió.
    """

    nombre = "falso"
    dias_de_pronostico = 16

    def __init__(self, *, probabilidad_lluvia: int = 10, codigo_clima: int = 1) -> None:
        self.probabilidad_lluvia = probabilidad_lluvia
        self.codigo_clima = codigo_clima
        self.consultas: list[tuple[date, date]] = []

    def pronostico(self, desde: date, hasta: date) -> list[DiaClima]:
        self.consultas.append((desde, hasta))
        dias = (hasta - desde).days + 1
        return [
            DiaClima(
                fecha=desde + timedelta(days=n),
                codigo_clima=self.codigo_clima,
                temperatura_max=27.0,
                temperatura_min=19.0,
                probabilidad_lluvia=self.probabilidad_lluvia,
            )
            for n in range(dias)
        ]


def obtener_proveedor_clima() -> ProveedorClima:
    """Dependencia de FastAPI: el proveedor configurado en ``CLIMA_PROVEEDOR``."""
    configuracion = obtener_configuracion()
    if configuracion.clima_proveedor == "falso":
        return ClimaFalso()
    from app.modulos.clima.open_meteo import ClimaOpenMeteo  # solo se carga si se usa

    return ClimaOpenMeteo(configuracion)
