"""
Path: src/infrastructure/fastapi/dinamic_server.py
"""

from typing import Optional

from fastapi import APIRouter, Query

from src.shared.config import get_config
from src.shared.logger import get_logger

from src.infrastructure.requests.xubio_client import SimpleXubioGateway
from src.interface_adapter.controllers.cliente_bean_controller import ClienteBeanController
from src.interface_adapter.controllers.obtener_token_controller import ObtenerTokenController
from src.infrastructure.requests.xubio_client import XubioClient
from src.interface_adapter.controllers.producto_venta_controller import ProductoVentaController

router = APIRouter(prefix="", tags=["xubio"])
logger = get_logger("xubio-adapter")

logger.info("Inicializando el router de Xubio Adapter")
logger.debug("Configuración inicial del router: prefix='', tags=['xubio']")

@router.post("/api/xubio/token/test")
@router.get("/api/xubio/token/test")
def token_test():
    "Endpoint de prueba para obtener un token de Xubio"
    logger.info("Endpoint /api/xubio/token/test llamado")
    cfg = get_config()
    token_gateway = XubioClient(cfg, logger)
    controller = ObtenerTokenController(token_gateway, logger)
    return controller.obtener_token()

@router.get("/api/xubio/clienteBean")
def get_cliente(updated_since: Optional[str] = Query(default=None, description="ISO date (YYYY-MM-DD)")):
    "Lista clientes desde Xubio, opcionalmente filtrando por fecha de actualización"
    logger.info("Endpoint /api/xubio/clienteBean llamado")
    cfg = get_config()
    gateway = SimpleXubioGateway(cfg, logger)
    controller = ClienteBeanController(gateway)
    return controller.get_cliente(updated_since)

@router.get("/api/xubio/clienteBean/{cliente_id}")
def get_cliente_by_id(cliente_id: str):
    "Obtiene un cliente específico por ID desde Xubio"
    logger.info("Endpoint /api/xubio/clienteBean/{cliente_id} llamado")
    cfg = get_config()
    gateway = SimpleXubioGateway(cfg, logger)
    controller = ClienteBeanController(gateway)
    return controller.get_cliente_by_id(cliente_id)

@router.get("/api/xubio/productos-venta")
def listar_productos_venta(updated_since: Optional[str] = Query(default=None, description="ISO date (YYYY-MM-DD)")):
    "Lista productos en venta desde Xubio, opcionalmente filtrando por fecha de actualización"
    logger.info("Endpoint /api/xubio/productos-venta llamado")
    cfg = get_config()
    gateway = SimpleXubioGateway(cfg, logger)
    controller = ProductoVentaController(gateway)
    return controller.listar_productos_venta(updated_since)
    
@router.get("/api/xubio/productos-venta/{cliente_id}")
def listar_productos_venta_by_id(cliente_id: str):
    "Lista productos en venta desde Xubio, opcionalmente filtrando por fecha de actualización"
    logger.info("Endpoint /api/xubio/productos-venta/{cliente_id} llamado")
    cfg = get_config()
    gateway = SimpleXubioGateway(cfg, logger)
    controller = ProductoVentaController(gateway)
    return controller.listar_productos_venta_by_id(cliente_id)
