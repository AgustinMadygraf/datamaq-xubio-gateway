"""
Protocolo para obtención de token de Xubio.
"""
from typing import Protocol

class TokenGateway(Protocol):
    "Protocol para obtención de token de Xubio."
    def get_access_token(self) -> dict:
        "Obtiene un token de acceso desde el sistema externo."
        pass # pylint: disable=unnecessary-pass
