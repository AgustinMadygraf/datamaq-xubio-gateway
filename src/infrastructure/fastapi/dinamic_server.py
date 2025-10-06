"""
Path: src/infrastructure/fastapi/dinamic_server.py
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from src.shared.config import get_config
from src.shared.logger import get_logger

from src.infrastructure.requests.xubio_client import XubioClient
from src.interface_adapter.gateways.xubio_gateway import XubioGateway
from src.interface_adapter.controllers.cliente_bean_controller import ClienteBeanController

router = APIRouter(prefix="", tags=["xubio"])
logger = get_logger("xubio-adapter")

logger.info("Inicializando el router de Xubio Adapter")
logger.debug("Configuración inicial del router: prefix='', tags=['xubio']")


# Subclase concreta de XubioGateway que delega en XubioClient
class SimpleXubioGateway(XubioGateway):
    "Implementación simple de XubioGateway usando XubioClient"
    def __init__(self, cfg, log):
        super().__init__()
        self._client = XubioClient(cfg, log)

    def cliente_bean(self, updated_since: Optional[str] = None):
        " Lista clientes desde Xubio, opcionalmente filtrando por fecha de actualización"
        return self._client.cliente_bean(updated_since)
    
    def get_cliente_by_id(self, cliente_id: str):
        "Obtiene un cliente por su ID usando XubioClient"
        return self._client.get_cliente_by_id(cliente_id)

@router.get("/api/xubio/clienteBean")
def cliente_bean(updated_since: Optional[str] = Query(default=None, description="ISO date (YYYY-MM-DD)")):
    "Lista clientes desde Xubio, opcionalmente filtrando por fecha de actualización"
    logger.info("Endpoint /api/xubio/clienteBean llamado")
    cfg = get_config()
    gateway = SimpleXubioGateway(cfg, logger)
    controller = ClienteBeanController(gateway)
    return controller.cliente_bean(updated_since)

@router.get("/api/xubio/clienteBean/{cliente_id}")
def get_cliente_by_id(cliente_id: str):
    "Obtiene un cliente específico por ID desde Xubio"
    logger.info("Endpoint /api/xubio/clienteBean/{cliente_id} llamado")
    cfg = get_config()
    gateway = SimpleXubioGateway(cfg, logger)
    controller = ClienteBeanController(gateway)
    return controller.get_cliente_by_id(cliente_id)

@router.post("/api/xubio/token/test")
@router.get("/api/xubio/token/test")
def token_test():
    "Endpoint de prueba para obtener un token de Xubio "
    logger.info("Endpoint /api/xubio/token/test llamado")
    try:
        cfg = get_config()
        client = XubioClient(cfg, logger)
        data = client.get_access_token()
        now = datetime.now(timezone.utc).isoformat()
        access = data.get("access_token", "")
        if not access:
            logger.warning("No se obtuvo access_token en la respuesta")
        masked = access[:6] + "…" + access[-4:] if isinstance(access, str) and len(access) > 12 else "mask"
        logger.debug("Token obtenido y enmascarado: %s", masked)
        return {
            "ok": True,
            "obtained_at_utc": now,
            "token_type": data.get("token_type", "Bearer"),
            "expires_in": data.get("expires_in"),
            "access_token_preview": masked,
        }
    except HTTPException as e:
        logger.error("Error en token_test: %s", e.detail)
        raise
    except Exception as e:
        logger.critical("Error inesperado en token_test: %s", e)
        raise HTTPException(status_code=500, detail="Error inesperado en token_test") from e
