"""Esquemas de salida del pronóstico del clima."""

from datetime import date

from pydantic import BaseModel, Field


class DiaPronosticoRespuesta(BaseModel):
    fecha: date
    disponible: bool = Field(
        description="False si el día está más allá de lo que el proveedor puede pronosticar."
    )
    descripcion: str | None = Field(None, examples=["Lluvia"])
    temperatura_max: float | None = Field(None, description="°C", examples=[27.4])
    temperatura_min: float | None = Field(None, description="°C", examples=[18.9])
    probabilidad_lluvia: int | None = Field(None, description="%", examples=[80])


class PronosticoRespuesta(BaseModel):
    fuente: str = Field(description="Proveedor que respondió.", examples=["open_meteo"])
    dias: list[DiaPronosticoRespuesta]
    dias_con_lluvia: list[date]
    umbral_lluvia: int = Field(description="Porcentaje desde el cual se avisa.", examples=[60])
    aviso: str | None = Field(
        None,
        examples=[
            "Probabilidad de lluvia de 60 % o más el día 20/11. Considera llevar impermeable."
        ],
    )
