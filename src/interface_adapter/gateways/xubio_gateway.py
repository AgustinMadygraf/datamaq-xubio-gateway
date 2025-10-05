"""
Path: src/interface_adapter/gateways/xubio_gateway.py
"""

from typing import Optional, Any

from src.infrastructure.requests.xubio_client import XubioClient
from src.use_cases.listar_clientes import XubioGateway
from src.use_cases.listar_productos_venta import XubioProductoVentaGateway

class XubioGatewayImpl(XubioGateway, XubioProductoVentaGateway):
    """
    Implementación del gateway de Xubio usando XubioClient.
    Permite desacoplar la infraestructura de los casos de uso.
    """
    def __init__(self, client: XubioClient):
        self.client = client

    def listar_clientes(self, updated_since: Optional[str] = None) -> Any:
        return self.client.listar_clientes(updated_since)

    def listar_productos_venta(self, updated_since: Optional[str] = None) -> Any:
        return self.client.listar_productos_venta(updated_since)
