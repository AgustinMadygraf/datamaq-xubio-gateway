"""
Path: src/use_cases/listar_clientes.py
"""

from typing import Optional, List
from src.entities.cliente import Cliente
from src.infrastructure.requests.xubio_client import XubioClient

class ListarClientesUseCase:
    "Caso de uso para listar clientes desde Xubio (acoplado a XubioClient)"
    def __init__(self, client: XubioClient):
        self.client = client

    def execute(self, updated_since: Optional[str] = None) -> List[Cliente]:
        "Lista clientes desde Xubio, opcionalmente filtrando por fecha de actualización"
        raw = self.client.listar_clientes(updated_since)
        items = raw.get("items") if isinstance(raw, dict) and "items" in raw else raw
        return [Cliente.from_dict(item) for item in items]
