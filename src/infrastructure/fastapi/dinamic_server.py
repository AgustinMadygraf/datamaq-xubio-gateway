"""
Path: src/infrastructure/fastapi/dinamic_server.py
"""

from datetime import datetime, timezone
from typing import Optional
import requests
from fastapi import APIRouter, HTTPException, Query

from src.shared.config import get_config, require_config
from src.shared.logger import get_logger

router = APIRouter(prefix="", tags=["xubio"])
logger = get_logger("xubio-adapter")

logger.info("Inicializando el router de Xubio Adapter")
logger.debug("Configuración inicial del router: prefix='', tags=['xubio']")


def _token_endpoint(cfg: dict) -> str:
    logger.debug("Entrando a _token_endpoint con cfg: %s", cfg)
    if not cfg.get("XUBIO_BASE_URL"):
        logger.warning("No se encontró XUBIO_BASE_URL en la configuración")
    if cfg.get("XUBIO_TOKEN_URL"):
        logger.info("Usando XUBIO_TOKEN_URL explícito")
        return cfg["XUBIO_TOKEN_URL"].rstrip("/")
    base = cfg["XUBIO_BASE_URL"].rstrip("/")
    logger.info("Usando base URL para construir endpoint de token")
    return f"{base}/1.1/oauth/token"


def _build_url(cfg: dict, path: str) -> str:
    logger.debug("Construyendo URL con base: %s y path: %s", cfg.get("XUBIO_BASE_URL"), path)
    if not path:
        logger.warning("El path para construir la URL está vacío")
    base = cfg["XUBIO_BASE_URL"].rstrip("/")
    path = path.lstrip("/")
    url = f"{base}/{path}"
    logger.info("URL construida: %s", url)
    return url


def _get_access_token() -> dict:
    logger.info("Obteniendo access token de Xubio")
    cfg = require_config(["XUBIO_BASE_URL", "XUBIO_CLIENT_ID", "XUBIO_CLIENT_SECRET"])
    token_url = _token_endpoint(cfg)
    try:
        logger.debug("Realizando POST a %s", token_url)
        resp = requests.post(
            token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": cfg["XUBIO_CLIENT_ID"],
                "client_secret": cfg["XUBIO_CLIENT_SECRET"],
            },
            timeout=cfg["XUBIO_TIMEOUT_S"],
            verify=cfg["XUBIO_VERIFY_TLS"],
        )
        logger.info("Respuesta de token recibida: status %s", resp.status_code)
        if resp.status_code == 401:
            logger.warning("Credenciales inválidas para Xubio (401 Unauthorized)")
        if resp.status_code >= 400:
            logger.error("Xubio token error %s: %s", resp.status_code, resp.text)
            raise HTTPException(status_code=resp.status_code, detail="Error al obtener token de Xubio")
        data = resp.json()
        logger.debug("Datos de token recibidos: %s", data)
        if "access_token" not in data:
            logger.error("Respuesta de token inesperada: %s", data)
            logger.critical("No se encontró 'access_token' en la respuesta de Xubio")
            raise HTTPException(status_code=502, detail="Token de Xubio sin 'access_token'")
        return data
    except requests.RequestException as e:
        logger.exception("Fallo HTTP al obtener token de Xubio")
        logger.critical("Excepción crítica al obtener token: %s", e)
        raise HTTPException(status_code=502, detail=f"Fallo HTTP token Xubio: {e}") from e


@router.post("/api/xubio/token/test")
def token_test():
    "Endpoint de prueba para obtener un token de Xubio "
    logger.info("Endpoint /api/xubio/token/test llamado")
    try:
        data = _get_access_token()
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
        data = _get_access_token()
        token = data["access_token"]
        path = cfg.get("XUBIO_CLIENTS_PATH")
        if not path:
            logger.warning("No se encontró XUBIO_CLIENTS_PATH en la configuración")
        url = _build_url(cfg, path)

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
    except requests.RequestException as e:
        logger.exception("Fallo HTTP consultando clientes en Xubio")
        logger.critical("Excepción crítica al consultar clientes: %s", e)
        raise HTTPException(status_code=502, detail=f"Fallo HTTP Xubio clientes: {e}") from e
    except Exception as e:
        logger.critical("Error inesperado en listar_clientes: %s", e)
        raise HTTPException(status_code=500, detail="Error inesperado en listar_clientes") from e
