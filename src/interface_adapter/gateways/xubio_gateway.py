"""
Path: src/interface_adapter/gateways/xubio_gateway.py
Gateway base para clientes usando Clean Architecture.
"""

from typing import Optional, List
from src.entities.cliente_bean_entitie import ClienteGateway, Cliente

class XubioGateway(ClienteGateway):
    """
    Gateway abstracto para interactuar con clientes (puede ser extendido o usado para mocks/tests).
    """
    def cliente_bean(self, updated_since: Optional[str] = None) -> List[Cliente]:
        """Lista clientes desde el sistema (debe ser implementado por subclases o mocks)."""
        raise NotImplementedError("Este método debe ser implementado por una subclase concreta.")
