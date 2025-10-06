"""
Path: src/interface_adapter/controllers/producto_venta_controller.py
"""
from typing import Optional
from fastapi import HTTPException
from src.shared.logger import get_logger
from src.interface_adapter.presenters.producto_venta_presenter import ProductoVentaPresenter
from src.use_cases.listar_productos_venta_use_case import ListarProductosVentaUseCase
from src.entities.producto_venta_entitie import ProductoVentaGateway

logger = get_logger("producto-venta-controller")

class ProductoVentaController:
    "Controller para manejar las solicitudes relacionadas con ProductoVenta"
    def __init__(self, gateway: ProductoVentaGateway):
        self.gateway = gateway
        self.logger = logger

    def listar_productos_venta(self, updated_since: Optional[str] = None):
        "Controlador para listar productos de venta, opcionalmente filtrando por fecha de actualización"
        self.logger.info("Controller: listar_productos_venta llamado")
        try:
            use_case = ListarProductosVentaUseCase(self.gateway)
            result = use_case.execute(updated_since)
            return ProductoVentaPresenter.list_to_dict(result)
        except Exception as e:
            self.logger.critical("Error inesperado en listar_productos_venta: %s", e)
            raise HTTPException(status_code=500, detail="Error inesperado en producto_venta_controller") from e

    def listar_productos_venta_by_id(self, cliente_id: str):
        "Controlador para listar productos de venta por ID de cliente"
        self.logger.info("Controller: listar_productos_venta_by_id llamado")
        try:
            from src.use_cases.get_producto_venta_by_id_use_case import GetProductoVentaByIdUseCase
            use_case = GetProductoVentaByIdUseCase(self.gateway)
            result = use_case.execute(cliente_id)
            return ProductoVentaPresenter.list_to_dict(result)
        except Exception as e:
            self.logger.critical("Error inesperado en listar_productos_venta_by_id: %s", e)
            raise HTTPException(status_code=500, detail="Error inesperado en producto_venta_controller") from e
