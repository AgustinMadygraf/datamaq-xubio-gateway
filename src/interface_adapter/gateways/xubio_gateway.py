"""
Path: src/interface_adapter/gateways/xubio_gateway.py
"""

from typing import Optional, Any

from src.infrastructure.requests.xubio_client import XubioClient
from src.use_cases.listar_clientes import XubioGateway

class XubioGatewayImpl(XubioGateway):
    """
    Implementación del gateway de Xubio usando XubioClient.
    Permite desacoplar la infraestructura de los casos de uso.
    """
    def __init__(self, client: XubioClient):
        self.client = client

    def listar_clientes(self, updated_since: Optional[str] = None) -> Any:
        return self.client.listar_clientes(updated_since)
