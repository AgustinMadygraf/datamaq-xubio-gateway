"""
Interfaz ClienteGateway para Clean Architecture.
"""
from typing import Optional, List, Protocol

class ClienteGateway(Protocol):
    " Puerto que define las operaciones para interactuar con clientes"
    def listar_clientes(self, updated_since: Optional[str] = None) -> List[dict]:
        "Lista clientes desde el sistema"
        pass # pylint: disable=unnecessary-pass
