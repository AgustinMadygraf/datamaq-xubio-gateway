"""
Path: src/use_cases/listar_clientes.py
"""

from typing import Optional, Protocol, Any

class XubioGateway(Protocol):
    "Protocolo para el gateway de Xubio"
    def listar_clientes(self, updated_since: Optional[str] = None) -> Any:
        "Lista clientes desde Xubio, opcionalmente filtrando por fecha de actualización"
        pass # pylint: disable=unnecessary-pass

class ListarClientesUseCase:
    "Caso de uso para listar clientes desde Xubio"
    def __init__(self, gateway: XubioGateway):
        self.gateway = gateway

    def execute(self, updated_since: Optional[str] = None):
        "Lista clientes desde Xubio, opcionalmente filtrando por fecha de actualización"
        return self.gateway.listar_clientes(updated_since)
