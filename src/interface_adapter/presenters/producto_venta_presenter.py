"""
Path: src/interface_adapter/presenters/producto_venta_presenter.py
"""

from src.entities.producto_venta_entitie import ProductoVenta

class ProductoVentaPresenter:
    "Presenter para formatear la salida de ProductoVenta"
    @staticmethod
    def to_dict(producto: ProductoVenta) -> dict:
        "Convierte una instancia de ProductoVenta a un diccionario."
        return producto.__dict__

    @staticmethod
    def list_to_dict(productos: list[ProductoVenta]) -> list[dict]:
        "Convierte una lista de ProductoVenta a una lista de diccionarios."
        return [ProductoVentaPresenter.to_dict(p) for p in productos]
