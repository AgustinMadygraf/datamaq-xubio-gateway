"""
Path: src/interface_adapter/controllers/cliente_controller.py
"""

from typing import Optional
from fastapi import HTTPException

from src.shared.config import get_config
from src.shared.logger import get_logger

from src.infrastructure.requests.xubio_client import XubioClient
from src.use_cases.listar_clientes import ListarClientesUseCase
from src.interface_adapter.presenters.cliente_presenter import ClientePresenter

logger = get_logger("cliente-controller")

def listar_clientes_controller(updated_since: Optional[str] = None):
    "Orquesta la obtención de clientes desde Xubio."
    logger.info("Controller: listar_clientes_controller llamado")
    cfg = get_config()
    try:
        gateway: XubioClient = XubioClient(cfg, logger)
        use_case = ListarClientesUseCase(gateway)
        result = use_case.execute(updated_since)
        return ClientePresenter.list_to_dict(result)
    except Exception as e:
        logger.critical("Error inesperado en listar_clientes_controller: %s", e)
        raise HTTPException(status_code=500, detail="Error inesperado en listar_clientes_controller") from e
