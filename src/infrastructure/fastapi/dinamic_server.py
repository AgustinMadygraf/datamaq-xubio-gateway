"""
Path: src/infrastructure/fastapi/dinamic_server.py
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from src.shared.config import get_config
from src.shared.logger import get_logger

from src.infrastructure.requests.xubio_client import XubioClient
from src.interface_adapter.gateways.xubio_gateway import XubioGatewayImpl
from src.use_cases.listar_clientes import ListarClientesUseCase
from src.use_cases.listar_productos_venta import ListarProductosVentaUseCase

router = APIRouter(prefix="", tags=["xubio"])
logger = get_logger("xubio-adapter")

logger.info("Inicializando el router de Xubio Adapter")
logger.debug("Configuración inicial del router: prefix='', tags=['xubio']")

@router.post("/api/xubio/token/test")
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


@router.get("/api/xubio/clientes")
def listar_clientes(updated_since: Optional[str] = Query(default=None, description="ISO date (YYYY-MM-DD)")):
    "Lista clientes desde Xubio, opcionalmente filtrando por fecha de actualización"
    logger.info("Endpoint /api/xubio/clientes llamado")
    cfg = get_config()
    try:
        client = XubioClient(cfg, logger)
        gateway = XubioGatewayImpl(client)
        use_case = ListarClientesUseCase(gateway)
        result = use_case.execute(updated_since)
        return result
    except Exception as e:
        logger.critical("Error inesperado en listar_clientes: %s", e)
        raise HTTPException(status_code=500, detail="Error inesperado en listar_clientes") from e


@router.get("/api/xubio/productos-venta")
def listar_productos_venta(updated_since: Optional[str] = Query(default=None, description="ISO date (YYYY-MM-DD)")):
    "Lista productos de venta desde Xubio, opcionalmente filtrando por fecha de actualización"
    logger.info("Endpoint /api/xubio/productos-venta llamado")
    cfg = get_config()
    try:
        client = XubioClient(cfg, logger)
        gateway = XubioGatewayImpl(client)
        use_case = ListarProductosVentaUseCase(gateway)
        result = use_case.execute(updated_since)
        return result
    except Exception as e:
        logger.critical("Error inesperado en listar_productos_venta: %s", e)
        raise HTTPException(status_code=500, detail="Error inesperado en listar_productos_venta") from e
