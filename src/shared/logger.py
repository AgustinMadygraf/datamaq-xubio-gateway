"""
Path: src/shared/logger.py
"""

import logging
from src.shared.config import get_config

class FastAPIStyleFormatter(logging.Formatter):
    """
    Formatter inspirado en FastAPI: [timestamp] [LEVEL] logger_name: message
    Mantiene colores por nivel para facilitar lectura en consola.
    """
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[41m', # Red background
    }
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        fmt = f"{color}[%(asctime)s] [%(levelname)s] %(name)s: %(message)s{self.RESET}"
        formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

def get_logger(name="datamaq-xubio-gateway"):
    """
    Configura y devuelve un logger con formato estilo FastAPI.
    """
    config = get_config()
    log_level = config.get("LOG_LEVEL", "DEBUG").upper()
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(FastAPIStyleFormatter())
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, log_level, logging.DEBUG))
    return logger
