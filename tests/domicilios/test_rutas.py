"""Rutas de domicilios: permisos y forma de las respuestas (HU-06).

Las reglas se prueban en ``test_servicio.py``; aquí solo el contrato HTTP.
"""

from datetime import timedelta

import pytest

from app.comun import fechas
from app.modulos.domicilios.estados import TRANSICIONES, es_transicion_valida
from app.modulos.domicilios.modelos import EstadoDomicilio
from app.modulos.pagos.modelos import MetodoPago
from app.modulos.usuarios.modelos import Rol
from tests.conftest import encabezado_de

PUNTO = {"latitud": "7.119300", "longitud": "-73.122700"}


@pytest.fixture
def reserva(sesion, fabrica, cliente_api) -> tuple[int, dict]:
    sesion.add(MetodoPago(codigo="tarjeta", nombre="Tarjeta"))
    fabrica.zona(tarifa_envio=5_000)
    modelo = fabrica.modelo(tarifa_diaria=30_000)
    fabrica.vehiculo(modelo)
    cliente = encabezado_de(fabrica.cliente())
    inicio = str(fechas.hoy() + timedelta(days=2))
    alquiler = cliente_api.post(
        "/alquileres",
        json={"modelo_id": modelo.id, "fecha_inicio": inicio, "fecha_fin": inicio},
        headers=cliente,
    ).json()
    return alquiler["id"], cliente


def test_zonas_y_cobertura_son_publicas(cliente_api, fabrica) -> None:
    fabrica.zona(tarifa_envio=5_000)

    zonas = cliente_api.get("/domicilios/zonas").json()
    cobertura = cliente_api.get("/domicilios/cobertura", params=PUNTO)
    fuera = cliente_api.get("/domicilios/cobertura", params={"latitud": 7.0, "longitud": -74.0})

    assert zonas["elementos"][0]["poligono"]["type"] == "Polygon"
    assert cobertura.json()["tarifa_envio"] == 5_000
    assert fuera.status_code == 422
    assert fuera.json()["error"]["codigo"] == "fuera_de_cobertura"


def test_flujo_solicitar_pagar_y_asignar(cliente_api, crear_usuario, reserva) -> None:
    alquiler_id, cliente = reserva
    operador = encabezado_de(crear_usuario(Rol.OPERADOR))
    domiciliario = crear_usuario(Rol.DOMICILIARIO)

    creado = cliente_api.post(
        "/domicilios",
        json={"alquiler_id": alquiler_id, "direccion": "Calle 36 # 19-20", **PUNTO},
        headers=cliente,
    )
    assert creado.status_code == 201
    domicilio = creado.json()
    assert (domicilio["valor_envio"], domicilio["total_operacion"]) == (5_000, 35_000)
    assert domicilio["estado"] == "pendiente"

    pago = cliente_api.post(
        f"/alquileres/{alquiler_id}/pago", json={"metodo_pago": "tarjeta"}, headers=cliente
    ).json()
    assert pago["pago"]["monto"] == 35_000

    disponibles = cliente_api.get("/domicilios/domiciliarios-disponibles", headers=operador).json()
    assert domiciliario.id in [d["id"] for d in disponibles["elementos"]]

    asignado = cliente_api.post(
        f"/domicilios/{domicilio['id']}/asignacion",
        json={"domiciliario_id": domiciliario.id},
        headers=operador,
    )
    assert asignado.status_code == 200
    assert asignado.json()["domiciliario"]["id"] == domiciliario.id

    entregas = cliente_api.get("/domicilios/asignados", headers=encabezado_de(domiciliario)).json()
    assert [e["id"] for e in entregas["elementos"]] == [domicilio["id"]]


def test_alquiler_y_venta_a_la_vez_es_invalido(cliente_api, reserva) -> None:
    alquiler_id, cliente = reserva
    respuesta = cliente_api.post(
        "/domicilios",
        json={"alquiler_id": alquiler_id, "venta_id": 1, "direccion": "Calle 36 # 19-20", **PUNTO},
        headers=cliente,
    )
    assert respuesta.status_code == 422


def test_permisos(cliente_api, crear_usuario, reserva) -> None:
    _, cliente = reserva
    domiciliario = encabezado_de(crear_usuario(Rol.DOMICILIARIO))
    assert cliente_api.get("/domicilios", headers=cliente).status_code == 403
    assert (
        cliente_api.get("/domicilios/domiciliarios-disponibles", headers=domiciliario).status_code
        == 403
    )
    assert cliente_api.get("/domicilios/asignados", headers=cliente).status_code == 403
    respuesta = cliente_api.post(
        "/domicilios/1/asignacion", json={"domiciliario_id": 1}, headers=cliente
    )
    assert respuesta.status_code == 403


# --- Transiciones (lógica pura) ---------------------------------------------------------------

E = EstadoDomicilio


def test_el_camino_normal_de_una_entrega() -> None:
    camino = [E.PENDIENTE, E.ASIGNADO, E.RECOGIDO, E.EN_CAMINO, E.ENTREGADO]
    assert all(es_transicion_valida(a, b) for a, b in zip(camino, camino[1:], strict=False))


@pytest.mark.parametrize("estado", [E.PENDIENTE, E.ASIGNADO, E.RECOGIDO, E.EN_CAMINO])
def test_cualquiera_salvo_entregado_se_puede_cancelar(estado) -> None:
    assert es_transicion_valida(estado, E.CANCELADO)


def test_entregado_y_cancelado_son_terminales() -> None:
    assert not TRANSICIONES[E.ENTREGADO] and not TRANSICIONES[E.CANCELADO]


def test_no_se_salta_pasos() -> None:
    assert not es_transicion_valida(E.PENDIENTE, E.EN_CAMINO)
    assert not es_transicion_valida(E.ASIGNADO, E.ENTREGADO)


# --- Consulta y cancelación del cliente por HTTP -------------------------------------------


def _solicitar(cliente_api, reserva) -> dict:
    alquiler_id, cliente = reserva
    creado = cliente_api.post(
        "/domicilios",
        json={"alquiler_id": alquiler_id, "direccion": "Calle 36 # 19-20", **PUNTO},
        headers=cliente,
    )
    assert creado.status_code == 201
    return creado.json()


def test_el_cliente_ve_sus_domicilios_y_el_detalle(cliente_api, crear_usuario, reserva) -> None:
    _, cliente = reserva
    domicilio = _solicitar(cliente_api, reserva)

    mios = cliente_api.get("/domicilios/mios", headers=cliente)
    detalle = cliente_api.get(f"/domicilios/{domicilio['id']}", headers=cliente)
    ajeno = cliente_api.get(
        f"/domicilios/{domicilio['id']}", headers=encabezado_de(crear_usuario(Rol.CLIENTE))
    )

    assert mios.status_code == 200
    assert [d["id"] for d in mios.json()["elementos"]] == [domicilio["id"]]
    assert detalle.status_code == 200
    assert detalle.json()["codigo_rastreo"] == domicilio["codigo_rastreo"]
    assert ajeno.status_code == 404


def test_el_cliente_quita_el_domicilio_antes_de_pagar(cliente_api, reserva) -> None:
    alquiler_id, cliente = reserva
    domicilio = _solicitar(cliente_api, reserva)

    cancelado = cliente_api.post(f"/domicilios/{domicilio['id']}/cancelacion", headers=cliente)
    alquiler = cliente_api.get(f"/alquileres/{alquiler_id}", headers=cliente).json()

    assert cancelado.status_code == 200
    assert cancelado.json()["estado"] == "cancelado"
    assert alquiler["valor_envio"] == 0
    assert alquiler["total"] == alquiler["subtotal"]
