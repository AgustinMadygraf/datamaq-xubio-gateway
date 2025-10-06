"""
Path: src/infrastructure/requests/xubio_client.py
"""

from typing import Optional
import requests
from requests.auth import HTTPBasicAuth
from fastapi import HTTPException


from src.interface_adapter.gateways.xubio_gateway import XubioGateway
from src.entities.cliente_bean_entitie import ClienteGateway, Cliente
from src.entities.token_gateway import TokenGateway
from src.entities.producto_venta_entitie import ProductoVenta, ProductoVentaGateway

class XubioClient(ClienteGateway, TokenGateway, ProductoVentaGateway):
    "Cliente HTTP para interactuar con la API de Xubio"
    def get_producto_venta_by_cliente_id(self, cliente_id: str):
        "Obtiene productos de venta asociados a un cliente específico por ID desde Xubio (filtrado local)"
        self.logger.info("Listando productos de venta por cliente_id desde Xubio (filtrado local): %s", cliente_id)
        # Obtener todos los productos de venta
        productos = self.get_producto_venta()
        # Filtrar localmente por el campo que relacione producto y cliente
        # Suponemos que el campo usrcode representa el cliente_id (ajustar si es otro campo)
        filtrados = [p for p in productos if str(p.usrcode) == str(cliente_id)]
        self.logger.info("Productos filtrados por cliente_id=%s: %d encontrados", cliente_id, len(filtrados))
        return filtrados
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

    def get_cliente(self, updated_since: Optional[str] = None):
        " Alias para cliente_bean"
        self.logger.info("Listando clientes desde Xubio (updated_since=%s)", updated_since)
        token_data = self.get_access_token()
        access_token = token_data["access_token"]
        path = self.cfg.get("XUBIO_CLIENTS_PATH", "/1.1/contacts")
        url = self.build_url(path)
        params = {}
        if updated_since:
            params["updated_since"] = updated_since
        try:
            resp = requests.get(
                url,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
                params=params,
                timeout=self.cfg["XUBIO_TIMEOUT_S"],
                verify=self.cfg["XUBIO_VERIFY_TLS"],
            )
            self.logger.info("Respuesta de clientes recibida: status %s", resp.status_code)
            if resp.status_code >= 400:
                self.logger.error("Error al listar clientes %s: %s", resp.status_code, resp.text)
                raise HTTPException(status_code=resp.status_code, detail="Error al listar clientes de Xubio")
            data = resp.json()
            items = data.get("items") if isinstance(data, dict) and "items" in data else data
            return [Cliente.from_dict(item) for item in items]
        except requests.RequestException as e:
            self.logger.exception("Fallo HTTP al listar clientes de Xubio")
            raise HTTPException(status_code=502, detail=f"Fallo HTTP listar clientes Xubio: {e}") from e

    def get_cliente_by_id(self, cliente_id: str):
        "Obtiene un cliente específico por ID desde Xubio"
        self.logger.info("Obteniendo cliente por ID desde Xubio: %s", cliente_id)
        token_data = self.get_access_token()
        access_token = token_data["access_token"]
        path = self.cfg.get("XUBIO_CLIENTS_PATH", "/1.1/clienteBean")
        url = self.build_url(f"{path}/{cliente_id}")
        try:
            resp = requests.get(
                url,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
                timeout=self.cfg["XUBIO_TIMEOUT_S"],
                verify=self.cfg["XUBIO_VERIFY_TLS"],
            )
            self.logger.info("Respuesta de cliente por ID recibida: status %s", resp.status_code)
            if resp.status_code == 404:
                self.logger.warning("Cliente no encontrado: %s", cliente_id)
                raise HTTPException(status_code=404, detail="Cliente no encontrado")
            if resp.status_code >= 400:
                self.logger.error("Error al obtener cliente %s: %s", resp.status_code, resp.text)
                raise HTTPException(status_code=resp.status_code, detail="Error al obtener cliente de Xubio")
            data = resp.json()
            return Cliente.from_dict(data)
        except requests.RequestException as e:
            self.logger.exception("Fallo HTTP al obtener cliente de Xubio")
            raise HTTPException(status_code=502, detail=f"Fallo HTTP obtener cliente Xubio: {e}") from e

    def get_producto_venta(self, updated_since: Optional[str] = None):
        "Lista productos de venta desde Xubio, opcionalmente filtrando por fecha de actualización"
        self.logger.info("Listando productos de venta desde Xubio (updated_since=%s)", updated_since)
        token_data = self.get_access_token()
        access_token = token_data["access_token"]
        path = self.cfg.get("XUBIO_PRODUCTOS_VENTA_PATH", "/1.1/ProductoVentaBean")
        url = self.build_url(path)
        params = {}
        if updated_since:
            params["updated_since"] = updated_since
        try:
            resp = requests.get(
                url,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
                params=params,
                timeout=self.cfg["XUBIO_TIMEOUT_S"],
                verify=self.cfg["XUBIO_VERIFY_TLS"],
            )
            self.logger.info("Respuesta de productos de venta recibida: status %s", resp.status_code)
            if resp.status_code >= 400:
                self.logger.error("Error al listar productos de venta %s: %s", resp.status_code, resp.text)
                raise HTTPException(
                    status_code=resp.status_code,
                    detail=f"Error al listar productos de venta de Xubio: {resp.text}"
                )
            data = resp.json()
            items = data.get("items") if isinstance(data, dict) and "items" in data else data
            return [ProductoVenta.from_dict(item) for item in items]
        except requests.RequestException as e:
            self.logger.exception("Fallo HTTP al listar productos de venta de Xubio")
            raise HTTPException(status_code=502, detail=f"Fallo HTTP listar productos de venta Xubio: {e}") from e

class SimpleXubioGateway(XubioGateway):
    "Implementación simple de XubioGateway usando XubioClient"
    def get_producto_venta_by_cliente_id(self, cliente_id: str):
        "Obtiene productos de venta asociados a un cliente específico por ID desde Xubio"
        return self._client.get_producto_venta_by_cliente_id(cliente_id)
    def __init__(self, cfg, log):
        super().__init__()
        self._client = XubioClient(cfg, log)

    def get_cliente(self, updated_since: Optional[str] = None):
        " Lista clientes desde Xubio, opcionalmente filtrando por fecha de actualización"
        return self._client.get_cliente(updated_since)

    def get_cliente_by_id(self, cliente_id: str):
        "Obtiene un cliente por su ID usando XubioClient"
        return self._client.get_cliente_by_id(cliente_id)

    def get_producto_venta(self, updated_since: Optional[str] = None):
        "Lista productos de venta desde Xubio, opcionalmente filtrando por fecha de actualización"
        return self._client.get_producto_venta(updated_since)
