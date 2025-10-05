"""
Path: src/use_cases/listar_productos_venta.py
"""

from typing import Optional, Protocol, Any

class XubioProductoVentaGateway(Protocol):
    "Protocolo para el gateway de productos de venta de Xubio"
    def listar_productos_venta(self, updated_since: Optional[str] = None) -> Any:
        "Lista productos de venta desde Xubio, opcionalmente filtrando por fecha de actualización"
        pass # pylint: disable=unnecessary-pass

class ListarProductosVentaUseCase:
    "Caso de uso para listar productos de venta desde Xubio"
    def __init__(self, gateway: XubioProductoVentaGateway):
        self.gateway = gateway

    def execute(self, updated_since: Optional[str] = None):
        "Lista productos de venta desde Xubio, opcionalmente filtrando por fecha de actualización"
        return self.gateway.listar_productos_venta(updated_since)
