"""Rutas del pronóstico del clima (segunda API externa).

Pública, como el catálogo: el cliente la consulta antes de reservar.
"""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.comun.errores import respuestas_error
from app.db import SesionBD
from app.modulos.clima import servicio
from app.modulos.clima.esquemas import DiaPronosticoRespuesta, PronosticoRespuesta
from app.modulos.clima.proveedor import ProveedorClima, obtener_proveedor_clima

enrutador_clima = APIRouter(prefix="/clima", tags=["clima"])

Proveedor = Annotated[ProveedorClima, Depends(obtener_proveedor_clima)]


@enrutador_clima.get(
    "/pronostico",
    response_model=PronosticoRespuesta,
    summary="Pronóstico del clima para las fechas de un alquiler",
    responses={
        **respuestas_error(422),
        503: {"description": "El servicio del clima no respondió"},
    },
)
def pronostico(
    sesion: SesionBD,
    proveedor: Proveedor,
    fecha_inicio: Annotated[date, Query(description="Primer día del alquiler (AAAA-MM-DD).")],
    fecha_fin: Annotated[date, Query(description="Último día del alquiler, inclusive.")],
) -> PronosticoRespuesta:
    """Pronóstico diario de la ciudad (Open-Meteo) entre las dos fechas, con un aviso si se
    espera lluvia. Los días más allá de 16 días salen con ``disponible: false``. Público."""
    resultado = servicio.pronostico_para_alquiler(sesion, proveedor, fecha_inicio, fecha_fin)
    return PronosticoRespuesta(
        fuente=resultado.fuente,
        dias=[DiaPronosticoRespuesta(**vars(d)) for d in resultado.dias],
        dias_con_lluvia=resultado.dias_con_lluvia,
        umbral_lluvia=resultado.umbral_lluvia,
        aviso=resultado.aviso,
    )
