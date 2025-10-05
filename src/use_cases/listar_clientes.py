"""
Path: src/use_cases/listar_clientes.py
"""

from typing import Optional, Protocol, Any, List
from src.domain.cliente import Cliente

class XubioGateway(Protocol):
    "Protocolo para el gateway de Xubio"
    def listar_clientes(self, updated_since: Optional[str] = None) -> Any:
        "Lista clientes desde Xubio, opcionalmente filtrando por fecha de actualización"
        pass # pylint: disable=unnecessary-pass

class ListarClientesUseCase:
    "Caso de uso para listar clientes desde Xubio"
    def __init__(self, gateway: XubioGateway):
        self.gateway = gateway

    def execute(self, updated_since: Optional[str] = None) -> List[Cliente]:
        "Lista clientes desde Xubio, opcionalmente filtrando por fecha de actualización"
        raw = self.gateway.listar_clientes(updated_since)
        # Suponiendo que raw es una lista de dicts o un dict con 'items'
        items = raw.get("items") if isinstance(raw, dict) and "items" in raw else raw
        return [Cliente.from_dict(item) for item in items]
