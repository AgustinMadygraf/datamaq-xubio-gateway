"""
Path: src/entities/cliente.py
"""

from typing import Optional, List, Protocol

class Cliente:
    " Entidad que representa un cliente en el dominio"
    def __init__(
        self,
        cliente_id: str,
        nombre: str,
        email: Optional[str] = None,
        telefono: Optional[str] = None,
        actualizado_en: Optional[str] = None,
    ):
        self.cliente_id = cliente_id
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.actualizado_en = actualizado_en

    @classmethod
    def from_dict(cls, data: dict):
        """
        Crea una instancia de Cliente desde un diccionario.
        Este método solo debe usarse en gateways para adaptar respuestas externas.
        """
        return cls(
            cliente_id=str(data.get("id") or data.get("codigo") or ""),
            nombre=data.get("nombre") or data.get("name") or "",
            email=data.get("email"),
            telefono=data.get("telefono") or data.get("phone"),
            actualizado_en=data.get("updated_at") or data.get("actualizado_en"),
        )


class ClienteGateway(Protocol):
    " Puerto que define las operaciones para interactuar con clientes"
    def listar_clientes(self, updated_since: Optional[str] = None) -> List[Cliente]:
        "Lista clientes desde el sistema"
        pass  # pylint: disable=unnecessary-pass
