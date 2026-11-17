"""Errores de negocio del pronóstico del clima. Cada uno dice la causa y qué hacer."""

from fastapi import status

from app.comun.errores import ErrorDeNegocio


class RangoDeFechasInvalido(ErrorDeNegocio):
    codigo = "rango_de_fechas_invalido"
    mensaje = "La fecha final es anterior a la fecha inicial."
    accion = "Elige una fecha final igual o posterior a la inicial."
    estado_http = status.HTTP_422_UNPROCESSABLE_CONTENT


class FechaEnElPasado(ErrorDeNegocio):
    codigo = "fecha_en_el_pasado"
    mensaje = "No hay pronóstico para fechas que ya pasaron."
    accion = "Elige fechas desde hoy en adelante."
    estado_http = status.HTTP_422_UNPROCESSABLE_CONTENT


class RangoDemasiadoLargo(ErrorDeNegocio):
    codigo = "rango_demasiado_largo"
    mensaje = "El rango supera el máximo de días de un alquiler."
    accion = "Elige un rango de fechas más corto."
    estado_http = status.HTTP_422_UNPROCESSABLE_CONTENT


class ClimaNoDisponible(ErrorDeNegocio):
    codigo = "clima_no_disponible"
    mensaje = "El servicio del clima no respondió."
    accion = "Inténtalo en unos minutos. El pronóstico es informativo: puedes reservar igual."
    estado_http = status.HTTP_503_SERVICE_UNAVAILABLE
