"""
Path: src/use_cases/listar_clientes.py
"""

from typing import Optional, List

from src.entities.cliente import Cliente
from src.entities.cliente_gateway import ClienteGateway

class ListarClientesUseCase:
    "Caso de uso para listar clientes desde un gateway (desacoplado de infraestructura)"
    def __init__(self, gateway: ClienteGateway):
        self.gateway = gateway

    def execute(self, updated_since: Optional[str] = None) -> List[Cliente]:
        "Lista clientes desde el gateway, opcionalmente filtrando por fecha de actualización"
        raw = self.gateway.listar_clientes(updated_since)
        items = raw.get("items") if isinstance(raw, dict) and "items" in raw else raw
        return [Cliente.from_dict(item) for item in items]
