"""
Path: src/infrastructure/requests/xubio_client.py
"""
import requests
from requests.auth import HTTPBasicAuth
from fastapi import HTTPException

from src.shared.logger import get_logger

logger = get_logger("xubio-client")

class XubioClient:
    "Cliente para interactuar con la API de Xubio"
    def __init__(self, cfg: dict, client_logger):
        self.cfg = cfg
        self.logger = client_logger

    def _token_endpoint(self) -> str:
        self.logger.debug("Entrando a _token_endpoint con cfg: %s", self.cfg)
        if not self.cfg.get("XUBIO_BASE_URL"):
            self.logger.warning("No se encontró XUBIO_BASE_URL en la configuración")
        if self.cfg.get("XUBIO_TOKEN_URL"):
            self.logger.info("Usando XUBIO_TOKEN_URL explícito")
            return self.cfg["XUBIO_TOKEN_URL"].rstrip("/")
        base = self.cfg["XUBIO_BASE_URL"].rstrip("/")
        self.logger.info("Usando base URL para construir endpoint de token")
        return f"{base}/1.1/oauth/token"

    def build_url(self, path: str) -> str:
        "Construye una URL completa para la API de Xubio dado un path"
        self.logger.debug("Construyendo URL con base: %s y path: %s", self.cfg.get("XUBIO_BASE_URL"), path)
        if not path:
            self.logger.warning("El path para construir la URL está vacío")
        base = self.cfg["XUBIO_BASE_URL"].rstrip("/")
        path = path.lstrip("/")
        url = f"{base}/{path}"
        self.logger.info("URL construida: %s", url)
        return url

    def get_access_token(self) -> dict:
        "Obtiene un token de acceso de Xubio"
        self.logger.info("Obteniendo access token de Xubio")
        token_url = self._token_endpoint()
        try:
            self.logger.debug("Realizando POST a %s", token_url)
            resp = requests.post(
                token_url,
                data={
                    "grant_type": "client_credentials",
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                auth=HTTPBasicAuth(self.cfg["XUBIO_CLIENT_ID"], self.cfg["XUBIO_CLIENT_SECRET"]),
                timeout=self.cfg["XUBIO_TIMEOUT_S"],
                verify=self.cfg["XUBIO_VERIFY_TLS"],
            )
            self.logger.info("Respuesta de token recibida: status %s", resp.status_code)
            if resp.status_code == 401:
                self.logger.warning("Credenciales inválidas para Xubio (401 Unauthorized)")
            if resp.status_code >= 400:
                self.logger.error("Xubio token error %s: %s", resp.status_code, resp.text)
                raise HTTPException(status_code=resp.status_code, detail="Error al obtener token de Xubio")
            data = resp.json()
            self.logger.debug("Datos de token recibidos: %s", data)
            if "access_token" not in data:
                self.logger.error("Respuesta de token inesperada: %s", data)
                self.logger.critical("No se encontró 'access_token' en la respuesta de Xubio")
                raise HTTPException(status_code=502, detail="Token de Xubio sin 'access_token'")
            return data
        except requests.RequestException as e:
            self.logger.exception("Fallo HTTP al obtener token de Xubio")
            self.logger.critical("Excepción crítica al obtener token: %s", e)
            raise HTTPException(status_code=502, detail=f"Fallo HTTP token Xubio: {e}") from e
