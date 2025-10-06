"""
Path: src/interface_adapter/controllers/obtener_token_controller.py
Controlador para obtención de token de Xubio.
"""

from datetime import datetime, timezone
from fastapi import HTTPException

from src.entities.token_gateway import TokenGateway

class ObtenerTokenController:
    "Controlador orientado a objetos para la obtención de token de Xubio."
    def __init__(self, token_gateway: TokenGateway, logger):
        self.token_gateway = token_gateway
        self.logger = logger

    def obtener_token(self):
        "Obtiene un token de acceso desde Xubio y retorna detalles relevantes."
        try:
            data = self.token_gateway.get_access_token()
            now = datetime.now(timezone.utc).isoformat()
            access = data.get("access_token", "")
            if not access:
                self.logger.warning("No se obtuvo access_token en la respuesta")
            masked = access[:6] + "…" + access[-4:] if isinstance(access, str) and len(access) > 12 else "mask"
            self.logger.debug("Token obtenido y enmascarado: %s", masked)
            return {
                "ok": True,
                "obtained_at_utc": now,
                "token_type": data.get("token_type", "Bearer"),
                "expires_in": data.get("expires_in"),
                "access_token_preview": masked,
            }
        except HTTPException as e:
            self.logger.error("Error en obtener_token_controller: %s", e.detail)
            raise
        except Exception as e:
            self.logger.critical("Error inesperado en obtener_token_controller: %s", e)
            raise HTTPException(status_code=500, detail="Error inesperado en obtener_token_controller") from e
