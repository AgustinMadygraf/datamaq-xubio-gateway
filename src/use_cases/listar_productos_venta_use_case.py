"""
Path: src/use_cases/listar_productos_venta_use_case.py
"""

from typing import Optional, List
from src.entities.producto_venta_entitie import ProductoVenta, ProductoVentaGateway

class ListarProductosVentaUseCase:
    "Caso de uso para listar productos de venta desde Xubio."
    def __init__(self, gateway: ProductoVentaGateway):
        self.gateway = gateway

    def execute(self, updated_since: Optional[str] = None) -> List[ProductoVenta]:
        "Ejecuta el caso de uso para listar productos de venta"
        return self.gateway.get_producto_venta(updated_since)
