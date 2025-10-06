"""
Path: src/use_cases/get_cliente_by_id_use_case.py
"""

from src.entities.cliente_bean_entitie import ClienteGateway, Cliente

class GetClienteByIdUseCase:
    "Caso de uso para obtener un cliente por ID"
    def __init__(self, gateway: ClienteGateway):
        self.gateway = gateway

    def execute(self, cliente_id: str) -> Cliente:
        "Ejecuta el caso de uso para obtener un cliente por su ID"
        return self.gateway.get_cliente_by_id(cliente_id)
