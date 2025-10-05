"""
Path: src/infrastructure/fastapi/xubio_adapter.py
Descripción: Endpoints mínimos para probar autenticación y consumo de Xubio API
"""

from datetime import datetime, timezone
from typing import Optional
import requests
from fastapi import APIRouter, HTTPException, Query
from src.shared.config import get_config, require_config
from src.shared.logger import get_logger

router = APIRouter(prefix="", tags=["xubio"])
log = get_logger("xubio-adapter")


def _token_endpoint(cfg: dict) -> str:
    # Si no viene seteado, intentamos inferirlo de la base
    if cfg.get("XUBIO_TOKEN_URL"):
        return cfg["XUBIO_TOKEN_URL"].rstrip("/")
    base = cfg["XUBIO_BASE_URL"].rstrip("/")
    # Documentaciones suelen publicar /API/documentation/index.html y un token endpoint estilo /1.1/oauth/token
    # Lo dejamos configurable; por default probamos variante común:
    return f"{base}/1.1/oauth/token"


def _build_url(cfg: dict, path: str) -> str:
    base = cfg["XUBIO_BASE_URL"].rstrip("/")
    path = path.lstrip("/")
    return f"{base}/{path}"


def _get_access_token() -> dict:
    cfg = require_config(["XUBIO_BASE_URL", "XUBIO_CLIENT_ID", "XUBIO_CLIENT_SECRET"])
    token_url = _token_endpoint(cfg)
    try:
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
        if resp.status_code >= 400:
            log.error(f"Xubio token error {resp.status_code}: {resp.text}")
            raise HTTPException(status_code=resp.status_code, detail="Error al obtener token de Xubio")
        data = resp.json()
        # data esperado: { access_token, token_type, expires_in, ... }
        if "access_token" not in data:
            log.error(f"Respuesta de token inesperada: {data}")
            raise HTTPException(status_code=502, detail="Token de Xubio sin 'access_token'")
        return data
    except requests.RequestException as e:
        log.exception("Fallo HTTP al obtener token de Xubio")
        raise HTTPException(status_code=502, detail=f"Fallo HTTP token Xubio: {e}")


@router.post("/api/xubio/token/test")
def token_test():
    "Prueba de autenticación: obtiene token y devuelve metadatos (sin exponerlo completo)"
    data = _get_access_token()
    now = datetime.now(timezone.utc).isoformat()
    access = data.get("access_token", "")
    masked = access[:6] + "…" + access[-4:] if isinstance(access, str) and len(access) > 12 else "mask"
    return {
        "ok": True,
        "obtained_at_utc": now,
        "token_type": data.get("token_type", "Bearer"),
        "expires_in": data.get("expires_in"),
        "access_token_preview": masked,
    }


@router.get("/api/xubio/clientes")
def listar_clientes(updated_since: Optional[str] = Query(default=None, description="ISO date (YYYY-MM-DD)")):
    """
    Ejemplo de consumo autenticado:
    Llama a un recurso típico de clientes en Xubio (path configurable por .env).
    """
    cfg = get_config()
    data = _get_access_token()
    token = data["access_token"]
    path = cfg["XUBIO_CLIENTS_PATH"]  # p. ej. '1.1/clienteBean'
    url = _build_url(cfg, path)

    params = {}
    if updated_since:
        params["updated_since"] = updated_since  # si el API lo soporta

    try:
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
            params=params,
            timeout=cfg["XUBIO_TIMEOUT_S"],
            verify=cfg["XUBIO_VERIFY_TLS"],
        )
        if resp.status_code >= 400:
            log.error(f"Xubio clientes error {resp.status_code}: {resp.text}")
            raise HTTPException(status_code=resp.status_code, detail="Error al consultar clientes en Xubio")
        return resp.json()
    except requests.RequestException as e:
        log.exception("Fallo HTTP consultando clientes en Xubio")
        raise HTTPException(status_code=502, detail=f"Fallo HTTP Xubio clientes: {e}")
