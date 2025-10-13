"""
Path: run.py
Arranque del servicio con chequeos y logger
"""

import os
import sys
import uvicorn
import mysql.connector
from database import get_connection
from src.shared.config import get_config, require_config
from src.shared.logger import get_logger
# from src.main import app

log = get_logger("datamaq-run")

def _preflight():
    cfg = get_config()

    try:
        require_config(["XUBIO_BASE_URL", "XUBIO_CLIENT_ID", "XUBIO_CLIENT_SECRET"])
    except RuntimeError as e:
        log.error(str(e))
        sys.exit(1)

    # Chequeo de assets front (mismo comportamiento que antes, opcional)
    static_path = os.getenv("STATIC_PATH") or cfg.get("STATIC_PATH")
    if static_path and not os.path.isdir(static_path):
        log.warning("STATIC_PATH no existe: %s (solo aviso)", static_path)

if __name__ == "__main__":
    _preflight()
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "5000"))
    log.info("Iniciando DataMaq Gateway en http://%s:%s", host, port)
    uvicorn.run(
        "src.infrastructure.fastapi.static_server:app",
        host=host,
        port=port,
        reload=os.getenv("UVICORN_RELOAD", "true").lower() == "true"
    )

try:
    conn = get_connection()
    if conn is None:
        log.error("No se pudo conectar a MySQL: get_connection() devolvió None")
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        print("Conectado a:", cursor.fetchone())
except mysql.connector.Error as e:
    log.error("Error al conectar a MySQL: %s", str(e))
