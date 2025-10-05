"""
Path: src/shared/config.py
"""

import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    "Load configuration from environment variables"
    config = {
        # --- Logging ---
        "LOG_LEVEL": os.getenv('LOG_LEVEL'),

        # --- Xubio API ---
        # Base general del API y endpoints (token opcionalmente overrideable)
        "XUBIO_BASE_URL": os.getenv('XUBIO_BASE_URL', 'https://main.xubio.com/API'),
        "XUBIO_TOKEN_URL": os.getenv('XUBIO_TOKEN_URL'),  # si no se setea, se infiere desde BASE
        "XUBIO_CLIENT_ID": os.getenv('XUBIO_CLIENT_ID'),
        "XUBIO_CLIENT_SECRET": os.getenv('XUBIO_CLIENT_SECRET'),
        "XUBIO_TIMEOUT_S": int(os.getenv('XUBIO_TIMEOUT_S', '15')),
        "XUBIO_VERIFY_TLS": os.getenv('XUBIO_VERIFY_TLS', 'true').lower() == 'true',

        # Endpoints de recursos (overrideables por .env si cambian paths)
        "XUBIO_CLIENTS_PATH": os.getenv('XUBIO_CLIENTS_PATH', '1.1/clienteBean'),
        # Agregás más paths cuando avances: productos, comprobantes, etc.
    }
    return config


def require_config(keys: list[str]):
    "Lanza excepción si faltan claves críticas"
    cfg = get_config()
    missing = [k for k in keys if not cfg.get(k)]
    if missing:
        raise RuntimeError(f"Faltan variables de entorno requeridas: {', '.join(missing)}")
    return cfg
