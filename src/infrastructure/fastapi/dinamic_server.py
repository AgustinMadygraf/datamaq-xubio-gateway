"""
Path: src/infrastructure/fastapi/dinamic_server.py
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
import requests

from src.shared.config import get_config
from src.shared.logger import get_logger

from src.infrastructure.requests.xubio_client import XubioClient

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
        data = client.get_access_token()
        token = data["access_token"]
        path = cfg.get("XUBIO_CLIENTS_PATH")
        if not path:
            logger.warning("No se encontró XUBIO_CLIENTS_PATH en la configuración")
        url = client.build_url(path)

        params = {}
        if updated_since:
            params["updated_since"] = updated_since
            logger.debug("Parametro updated_since recibido: %s", updated_since)
        else:
            logger.info("No se recibió parámetro updated_since")

        logger.info("Realizando GET a %s con params %s", url, params)
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
            params=params,
            timeout=cfg["XUBIO_TIMEOUT_S"],
            verify=cfg["XUBIO_VERIFY_TLS"],
        )
        logger.info("Respuesta de clientes recibida: status %s", resp.status_code)
        if resp.status_code == 404:
            logger.warning("Endpoint de clientes no encontrado (404)")
        if resp.status_code >= 400:
            logger.error("Xubio clientes error %s: %s", resp.status_code, resp.text)
            raise HTTPException(status_code=resp.status_code, detail="Error al consultar clientes en Xubio")
        logger.debug("Datos de clientes recibidos: %s", resp.text)
        return resp.json()
    except Exception as e:
        logger.critical("Error inesperado en listar_clientes: %s", e)
        raise HTTPException(status_code=500, detail="Error inesperado en listar_clientes") from e
