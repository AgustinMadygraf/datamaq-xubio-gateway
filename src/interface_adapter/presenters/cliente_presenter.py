"""
Presentador para la entidad Cliente.
"""

from src.domain.cliente import Cliente

class ClientePresenter:
    @staticmethod
    def to_dict(cliente: Cliente) -> dict:
        return {
            "cliente_id": cliente.cliente_id,
            "nombre": cliente.nombre,
            "email": cliente.email,
            "telefono": cliente.telefono,
            "actualizado_en": cliente.actualizado_en,
        }

    @staticmethod
    def list_to_dict(clientes: list[Cliente]) -> list[dict]:
        return [ClientePresenter.to_dict(c) for c in clientes]
