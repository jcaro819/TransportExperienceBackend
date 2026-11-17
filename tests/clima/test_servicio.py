"""Reglas del pronóstico del clima para un alquiler (con el proveedor falso)."""

from datetime import date, timedelta

import pytest

from app.modulos.clima import servicio
from app.modulos.clima.excepciones import (
    FechaEnElPasado,
    RangoDeFechasInvalido,
    RangoDemasiadoLargo,
)
from app.modulos.clima.proveedor import ClimaFalso
from app.parametros import PORCENTAJE_LLUVIA_AVISO, ParametroSistema

HOY = date(2026, 11, 17)


def test_un_dia_por_fecha_inclusive_y_sin_aviso_si_no_llueve(sesion):
    resultado = servicio.pronostico_para_alquiler(
        sesion, ClimaFalso(probabilidad_lluvia=10), HOY, HOY + timedelta(days=2), hoy=HOY
    )
    assert [d.fecha for d in resultado.dias] == [HOY + timedelta(days=n) for n in range(3)]
    assert all(d.disponible for d in resultado.dias)
    assert resultado.dias[0].descripcion == "Parcialmente nublado"
    assert resultado.aviso is None
    assert resultado.dias_con_lluvia == []


def test_avisa_desde_el_umbral_guardado_en_la_base(sesion):
    sesion.get(ParametroSistema, PORCENTAJE_LLUVIA_AVISO).valor = 80
    sesion.flush()

    bajo = servicio.pronostico_para_alquiler(
        sesion, ClimaFalso(probabilidad_lluvia=79), HOY, HOY, hoy=HOY
    )
    alto = servicio.pronostico_para_alquiler(
        sesion, ClimaFalso(probabilidad_lluvia=80, codigo_clima=63), HOY, HOY, hoy=HOY
    )

    assert bajo.aviso is None
    assert alto.umbral_lluvia == 80
    assert alto.dias_con_lluvia == [HOY]
    assert alto.dias[0].descripcion == "Lluvia"
    assert "17/11" in alto.aviso


def test_los_dias_mas_alla_del_pronostico_no_se_le_piden_al_proveedor(sesion):
    proveedor = ClimaFalso()  # pronostica 16 días: de HOY a HOY + 15
    inicio = HOY + timedelta(days=14)
    resultado = servicio.pronostico_para_alquiler(
        sesion, proveedor, inicio, inicio + timedelta(days=3), hoy=HOY
    )
    assert proveedor.consultas == [(inicio, HOY + timedelta(days=15))]
    assert [d.disponible for d in resultado.dias] == [True, True, False, False]


def test_un_rango_totalmente_lejano_no_consulta_al_proveedor(sesion):
    proveedor = ClimaFalso()
    inicio = HOY + timedelta(days=20)
    resultado = servicio.pronostico_para_alquiler(sesion, proveedor, inicio, inicio, hoy=HOY)
    assert proveedor.consultas == []
    assert resultado.dias[0].disponible is False
    assert resultado.aviso is None


@pytest.mark.parametrize(
    ("inicio", "fin", "error"),
    [
        (HOY + timedelta(days=3), HOY + timedelta(days=1), RangoDeFechasInvalido),
        (HOY - timedelta(days=1), HOY + timedelta(days=1), FechaEnElPasado),
        (HOY, HOY + timedelta(days=30), RangoDemasiadoLargo),  # 31 días; el máximo es 30
    ],
)
def test_rangos_invalidos(sesion, inicio, fin, error):
    with pytest.raises(error):
        servicio.pronostico_para_alquiler(sesion, ClimaFalso(), inicio, fin, hoy=HOY)


@pytest.mark.parametrize(
    ("codigo", "texto"),
    [
        (0, "Despejado"),
        (3, "Nublado"),
        (45, "Niebla"),
        (81, "Chubascos"),
        (99, "Tormenta eléctrica"),
        (5, "Sin descripción"),
    ],
)
def test_descripcion_de_codigos_wmo(codigo, texto):
    assert servicio.descripcion_wmo(codigo) == texto
