"""
Path: src/use_cases/get_producto_venta_by_id_use_case.py
"""

from typing import List
from src.entities.producto_venta_entitie import ProductoVenta, ProductoVentaGateway

class GetProductoVentaByIdUseCase:
    "Caso de uso para obtener productos de venta por ID de cliente desde Xubio."
    def __init__(self, gateway: ProductoVentaGateway):
        self.gateway = gateway

    def execute(self, cliente_id: str) -> List[ProductoVenta]:
        "Obtiene productos de venta asociados a un cliente específico por ID."
        return self.gateway.get_producto_venta_by_cliente_id(cliente_id)
