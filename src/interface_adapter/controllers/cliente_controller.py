"""
Path: src/interface_adapter/controllers/cliente_controller.py
"""

from typing import Optional
from fastapi import HTTPException

from src.shared.logger import get_logger

from src.interface_adapter.presenters.cliente_presenter import ClientePresenter
from src.use_cases.listar_clientes import ListarClientesUseCase
from src.entities.cliente import ClienteGateway

logger = get_logger("cliente-controller")


class ClienteController:
    "Controller orientado a objetos para operaciones sobre clientes."
    def __init__(self, gateway: ClienteGateway):
        self.gateway = gateway
        self.logger = logger

    def listar_clientes(self, updated_since: Optional[str] = None):
        "Orquesta la obtención de clientes desde el gateway inyectado."
        self.logger.info("Controller: listar_clientes (POO) llamado")
        try:
            use_case = ListarClientesUseCase(self.gateway)
            result = use_case.execute(updated_since)
            return ClientePresenter.list_to_dict(result)
        except Exception as e:
            self.logger.critical("Error inesperado en listar_clientes (POO): %s", e)
            raise HTTPException(status_code=500, detail="Error inesperado en listar_clientes_controller") from e
