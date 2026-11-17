"""Pronóstico del clima para las fechas de un alquiler (segunda API externa).

Consume **Open-Meteo** (https://open-meteo.com): gratis y sin llave. Antes de reservar,
el cliente ve si se espera lluvia en Bucaramanga en los días que eligió, algo útil para
vehículos que se usan a la intemperie (ciclas, patines y monopatines).

Igual que la pasarela de pagos (``pagos/pasarela.py``), el resto del sistema solo conoce
la interfaz ``ProveedorClima``; ``CLIMA_PROVEEDOR`` en el ``.env`` escoge la
implementación real (``open_meteo``) o la falsa (``falso``), que no toca la red.
"""
