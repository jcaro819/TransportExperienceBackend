"""Reglas del pronóstico del clima para un alquiler (segunda API externa).

Las rutas solo validan la entrada y llaman aquí; este módulo nunca habla HTTP: le pide
los datos a un ``ProveedorClima`` (Open-Meteo o el falso).
"""

from dataclasses import dataclass
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.comun import fechas
from app.modulos.clima.excepciones import (
    FechaEnElPasado,
    RangoDeFechasInvalido,
    RangoDemasiadoLargo,
)
from app.modulos.clima.proveedor import DiaClima, ProveedorClima
from app.parametros import MAX_DIAS_ALQUILER, PORCENTAJE_LLUVIA_AVISO, obtener_entero

# Códigos WMO que usa Open-Meteo, agrupados en descripciones cortas para el cliente.
_DESCRIPCIONES_WMO: list[tuple[range, str]] = [
    (range(0, 1), "Despejado"),
    (range(1, 3), "Parcialmente nublado"),
    (range(3, 4), "Nublado"),
    (range(45, 49), "Niebla"),
    (range(51, 58), "Llovizna"),
    (range(61, 68), "Lluvia"),
    (range(71, 78), "Nieve"),
    (range(80, 83), "Chubascos"),
    (range(85, 87), "Chubascos de nieve"),
    (range(95, 100), "Tormenta eléctrica"),
]


def descripcion_wmo(codigo: int) -> str:
    """Texto corto para un código WMO; ``"Sin descripción"`` si no se reconoce."""
    for rango, texto in _DESCRIPCIONES_WMO:
        if codigo in rango:
            return texto
    return "Sin descripción"


@dataclass(frozen=True)
class DiaPronostico:
    fecha: date
    disponible: bool  # False: el día está más allá de lo que el proveedor pronostica
    descripcion: str | None = None
    temperatura_max: float | None = None
    temperatura_min: float | None = None
    probabilidad_lluvia: int | None = None


@dataclass(frozen=True)
class PronosticoAlquiler:
    fuente: str
    dias: list[DiaPronostico]
    dias_con_lluvia: list[date]
    umbral_lluvia: int
    aviso: str | None


def pronostico_para_alquiler(
    sesion: Session,
    proveedor: ProveedorClima,
    fecha_inicio: date,
    fecha_fin: date,
    *,
    hoy: date | None = None,
) -> PronosticoAlquiler:
    """Pronóstico día por día de un alquiler de ``fecha_inicio`` a ``fecha_fin`` (inclusive).

    Valida el rango con las mismas reglas de un alquiler (fechas inclusivas, desde hoy, máximo
    ``max_dias_alquiler`` días). Solo le pide al proveedor los días que puede pronosticar; los
    posteriores salen con ``disponible=False``. Si algún día supera ``porcentaje_lluvia_aviso``,
    devuelve un aviso para el cliente.
    """
    hoy = hoy or fechas.hoy()
    if fecha_fin < fecha_inicio:
        raise RangoDeFechasInvalido()
    if fecha_inicio < hoy:
        raise FechaEnElPasado()
    max_dias = obtener_entero(sesion, MAX_DIAS_ALQUILER)
    total_dias = (fecha_fin - fecha_inicio).days + 1
    if total_dias > max_dias:
        raise RangoDemasiadoLargo(
            f"El rango tiene {total_dias} días y el máximo de un alquiler es {max_dias}."
        )
    umbral = obtener_entero(sesion, PORCENTAJE_LLUVIA_AVISO)

    ultimo_pronosticable = hoy + timedelta(days=proveedor.dias_de_pronostico - 1)
    recibidos: dict[date, DiaClima] = {}
    if fecha_inicio <= ultimo_pronosticable:
        hasta = min(fecha_fin, ultimo_pronosticable)
        recibidos = {d.fecha: d for d in proveedor.pronostico(fecha_inicio, hasta)}

    dias: list[DiaPronostico] = []
    for n in range(total_dias):
        fecha = fecha_inicio + timedelta(days=n)
        dia = recibidos.get(fecha)
        if dia is None:
            dias.append(DiaPronostico(fecha=fecha, disponible=False))
        else:
            dias.append(
                DiaPronostico(
                    fecha=fecha,
                    disponible=True,
                    descripcion=descripcion_wmo(dia.codigo_clima),
                    temperatura_max=dia.temperatura_max,
                    temperatura_min=dia.temperatura_min,
                    probabilidad_lluvia=dia.probabilidad_lluvia,
                )
            )

    con_lluvia = [
        d.fecha
        for d in dias
        if d.probabilidad_lluvia is not None and d.probabilidad_lluvia >= umbral
    ]
    return PronosticoAlquiler(
        fuente=proveedor.nombre,
        dias=dias,
        dias_con_lluvia=con_lluvia,
        umbral_lluvia=umbral,
        aviso=_aviso(con_lluvia, umbral),
    )


def _aviso(dias_con_lluvia: list[date], umbral: int) -> str | None:
    if not dias_con_lluvia:
        return None
    lista = ", ".join(d.strftime("%d/%m") for d in dias_con_lluvia)
    plural = "los días" if len(dias_con_lluvia) > 1 else "el día"
    return (
        f"Probabilidad de lluvia de {umbral} % o más {plural} {lista}. "
        "Considera llevar impermeable o elegir otras fechas."
    )
