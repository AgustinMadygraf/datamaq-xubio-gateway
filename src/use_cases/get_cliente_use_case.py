"""
Path: src/use_cases/get_cliente_use_case.py
"""

from typing import Optional, List

from src.entities.cliente_bean_entitie import Cliente, ClienteGateway

class ListarClientesUseCase:
    "Caso de uso para listar clientes desde un gateway (desacoplado de infraestructura)"
    def __init__(self, gateway: ClienteGateway):
        self.gateway = gateway

    def execute(self, updated_since: Optional[str] = None) -> List[Cliente]:
        "Lista clientes desde el gateway, opcionalmente filtrando por fecha de actualización"
        return self.gateway.get_cliente(updated_since)
