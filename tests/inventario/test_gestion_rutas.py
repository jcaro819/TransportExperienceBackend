"""Rutas de la gestión del inventario (HU-10): permisos y forma de las respuestas."""

import pytest

from app.modulos.usuarios.modelos import Rol
from tests.conftest import encabezado_de


@pytest.fixture
def admin(crear_usuario):
    return encabezado_de(crear_usuario(Rol.ADMINISTRADOR))


def test_el_administrador_arma_el_inventario_por_la_api(cliente_api, admin) -> None:
    tipo = cliente_api.post(
        "/inventario/tipos", json={"nombre": "Scooter", "usa_bateria": True}, headers=admin
    )
    assert tipo.status_code == 201
    modelo = cliente_api.post(
        "/inventario/modelos",
        json={
            "tipo_vehiculo_id": tipo.json()["id"],
            "nombre": "Scooter 300",
            "tarifa_diaria": 35000,
        },
        headers=admin,
    )
    assert modelo.status_code == 201
    unidad = cliente_api.post(
        "/inventario/unidades",
        json={"codigo": "sco-0001", "modelo_id": modelo.json()["id"], "nivel_bateria": 100},
        headers=admin,
    )
    assert unidad.status_code == 201
    assert (unidad.json()["codigo"], unidad.json()["estado"]) == ("SCO-0001", "disponible")

    catalogo = cliente_api.get("/catalogo/modelos").json()
    assert "Scooter 300" in [m["nombre"] for m in catalogo["elementos"]]


def test_producto_ajuste_y_alerta(cliente_api, admin) -> None:
    producto = cliente_api.post(
        "/inventario/productos",
        json={
            "codigo": "REP-LLANTA",
            "nombre": "Llanta 10 pulgadas",
            "categoria": "repuesto",
            "precio_venta": 85000,
            "stock": 4,
            "stock_minimo": 2,
        },
        headers=admin,
    ).json()
    assert producto["bajo_stock"] is False

    ajustado = cliente_api.post(
        f"/inventario/productos/{producto['id']}/ajustes",
        json={"cantidad": -2, "motivo": "Dos llantas pinchadas."},
        headers=admin,
    ).json()
    assert (ajustado["stock"], ajustado["bajo_stock"]) == (2, True)

    alertas = cliente_api.get("/inventario/alertas-stock", headers=admin).json()
    assert [p["codigo"] for p in alertas["elementos"]] == ["REP-LLANTA"]


def test_codigo_duplicado_con_error_uniforme(cliente_api, admin, fabrica) -> None:
    fabrica.vehiculo(codigo="MON-0001")
    respuesta = cliente_api.post(
        "/inventario/unidades",
        json={"codigo": "MON-0001", "modelo_id": fabrica.modelo().id},
        headers=admin,
    )
    assert respuesta.status_code == 409
    assert respuesta.json()["error"]["codigo"] == "codigo_duplicado"


@pytest.mark.parametrize(
    ("rol", "lectura", "escritura"),
    [(Rol.OPERADOR, 200, 403), (Rol.CLIENTE, 403, 403), (Rol.DOMICILIARIO, 403, 403)],
)
def test_permisos(cliente_api, crear_usuario, rol, lectura, escritura) -> None:
    encabezado = encabezado_de(crear_usuario(rol))
    assert cliente_api.get("/inventario/resumen", headers=encabezado).status_code == lectura
    assert cliente_api.get("/inventario/alertas-stock", headers=encabezado).status_code == lectura
    crear = cliente_api.post(
        "/inventario/tipos", json={"nombre": "Scooter", "usa_bateria": True}, headers=encabezado
    )
    assert crear.status_code == escritura


def test_el_resumen_trae_todos_los_estados(cliente_api, admin, fabrica) -> None:
    fabrica.vehiculo()
    resumen = cliente_api.get("/inventario/resumen", headers=admin).json()
    assert resumen["unidades_por_estado"]["disponible"] == 1
    assert resumen["unidades_por_estado"]["vendido"] == 0


# --- Edición (PATCH) por HTTP ---------------------------------------------------------------


def test_editar_tipo_por_http(cliente_api, admin, fabrica) -> None:
    tipo = fabrica.tipo()
    respuesta = cliente_api.patch(
        f"/inventario/tipos/{tipo.id}", json={"nombre": "Patineta eléctrica"}, headers=admin
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["nombre"] == "Patineta eléctrica"


def test_editar_modelo_por_http_y_sacarlo_del_alquiler(cliente_api, admin, fabrica) -> None:
    modelo = fabrica.modelo(tarifa_diaria=30_000, precio_venta=900_000)
    respuesta = cliente_api.patch(
        f"/inventario/modelos/{modelo.id}",
        json={"nombre": "Volt City S3", "tarifa_diaria": None},
        headers=admin,
    )
    assert respuesta.status_code == 200
    assert (respuesta.json()["nombre"], respuesta.json()["tarifa_diaria"]) == ("Volt City S3", None)


def test_un_modelo_no_queda_sin_tarifa_ni_precio(cliente_api, admin, fabrica) -> None:
    modelo = fabrica.modelo(tarifa_diaria=30_000, precio_venta=None)
    respuesta = cliente_api.patch(
        f"/inventario/modelos/{modelo.id}", json={"tarifa_diaria": None}, headers=admin
    )
    assert respuesta.status_code == 422


def test_editar_unidad_por_http(cliente_api, admin, fabrica) -> None:
    unidad = fabrica.vehiculo()
    respuesta = cliente_api.patch(
        f"/inventario/unidades/{unidad.id}",
        json={"ubicacion": "Sede Cabecera", "observaciones": "Rayón en el guardabarros."},
        headers=admin,
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["ubicacion"] == "Sede Cabecera"


def test_editar_producto_por_http(cliente_api, admin, fabrica) -> None:
    producto = fabrica.producto()
    respuesta = cliente_api.patch(
        f"/inventario/productos/{producto.id}",
        json={"precio_venta": 99_000, "stock_minimo": 5},
        headers=admin,
    )
    assert respuesta.status_code == 200
    assert (respuesta.json()["precio_venta"], respuesta.json()["stock_minimo"]) == (99_000, 5)


def test_editar_lo_que_no_existe_es_404(cliente_api, admin) -> None:
    for ruta in (
        "/inventario/tipos/999999",
        "/inventario/modelos/999999",
        "/inventario/unidades/999999",
        "/inventario/productos/999999",
    ):
        respuesta = cliente_api.patch(ruta, json={"nombre": "Algo válido"}, headers=admin)
        assert respuesta.status_code in (404, 422), ruta


def test_nulo_en_campo_obligatorio_es_422(cliente_api, admin, fabrica) -> None:
    tipo = fabrica.tipo()
    respuesta = cliente_api.patch(
        f"/inventario/tipos/{tipo.id}", json={"nombre": None}, headers=admin
    )
    assert respuesta.status_code == 422


@pytest.mark.parametrize("rol", [Rol.OPERADOR, Rol.CLIENTE, Rol.DOMICILIARIO])
def test_solo_el_administrador_edita(cliente_api, crear_usuario, fabrica, rol) -> None:
    encabezado = encabezado_de(crear_usuario(rol))
    tipo, modelo, unidad, producto = (
        fabrica.tipo(),
        fabrica.modelo(),
        fabrica.vehiculo(),
        fabrica.producto(),
    )
    assert (
        cliente_api.patch(
            f"/inventario/tipos/{tipo.id}", json={"nombre": "Otro"}, headers=encabezado
        ).status_code
        == 403
    )
    assert (
        cliente_api.patch(
            f"/inventario/modelos/{modelo.id}", json={"nombre": "Otro"}, headers=encabezado
        ).status_code
        == 403
    )
    assert (
        cliente_api.patch(
            f"/inventario/unidades/{unidad.id}", json={"ubicacion": "Otra"}, headers=encabezado
        ).status_code
        == 403
    )
    assert (
        cliente_api.patch(
            f"/inventario/productos/{producto.id}", json={"nombre": "Otro"}, headers=encabezado
        ).status_code
        == 403
    )


def test_listados_de_gestion_por_http(cliente_api, admin, fabrica) -> None:
    fabrica.vehiculo()
    fabrica.producto(nombre="Casco urbano")

    tipos = cliente_api.get("/inventario/tipos", headers=admin)
    modelos = cliente_api.get("/inventario/modelos", headers=admin)
    productos = cliente_api.get("/inventario/productos", headers=admin)

    for respuesta in (tipos, modelos, productos):
        assert respuesta.status_code == 200
        assert respuesta.json()["total"] >= 1  # paginados, como toda lista
    assert "Casco urbano" in [p["nombre"] for p in productos.json()["elementos"]]
