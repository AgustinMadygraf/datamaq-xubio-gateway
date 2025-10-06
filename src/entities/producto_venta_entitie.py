"""
Path: src/entities/producto_venta_entitie.py
"""
from typing import Optional, Protocol, List

class ProductoVenta:
    "Entidad que representa un producto de venta en Xubio."
    def __init__(
        self,
        productoid: int,
        nombre: str,
        codigo: Optional[str] = None,
        usrcode: Optional[str] = None,
        codigoBarra: Optional[str] = None,
        unidadMedida: Optional[dict] = None,
        categoria: Optional[int] = None,
        stockNegativo: Optional[bool] = None,
        tasaIva: Optional[dict] = None,
        cuentaContable: Optional[dict] = None,
        catFormIVA2002: Optional[int] = None,
        precioUltCompra: Optional[float] = None,
        activo: Optional[int] = None,
        actividadEconomica: Optional[dict] = None,
        sincronizaStock: Optional[int] = None,
        noObjetoImpuesto: Optional[int] = None,
        tipoOperacionIvaSimple: Optional[int] = None,
    ):
        self.productoid = productoid
        self.nombre = nombre
        self.codigo = codigo
        self.usrcode = usrcode
        self.codigoBarra = codigoBarra
        self.unidadMedida = unidadMedida
        self.categoria = categoria
        self.stockNegativo = stockNegativo
        self.tasaIva = tasaIva
        self.cuentaContable = cuentaContable
        self.catFormIVA2002 = catFormIVA2002
        self.precioUltCompra = precioUltCompra
        self.activo = activo
        self.actividadEconomica = actividadEconomica
        self.sincronizaStock = sincronizaStock
        self.noObjetoImpuesto = noObjetoImpuesto
        self.tipoOperacionIvaSimple = tipoOperacionIvaSimple

    @classmethod
    def from_dict(cls, data: dict):
        "Crea una instancia de ProductoVenta a partir de un diccionario."
        return cls(
            productoid=data.get("productoid"),
            nombre=data.get("nombre"),
            codigo=data.get("codigo"),
            usrcode=data.get("usrcode"),
            codigoBarra=data.get("codigoBarra"),
            unidadMedida=data.get("unidadMedida"),
            categoria=data.get("categoria"),
            stockNegativo=data.get("stockNegativo"),
            tasaIva=data.get("tasaIva"),
            cuentaContable=data.get("cuentaContable"),
            catFormIVA2002=data.get("catFormIVA2002"),
            precioUltCompra=data.get("precioUltCompra"),
            activo=data.get("activo"),
            actividadEconomica=data.get("actividadEconomica"),
            sincronizaStock=data.get("sincronizaStock"),
            noObjetoImpuesto=data.get("noObjetoImpuesto"),
            tipoOperacionIvaSimple=data.get("tipoOperacionIvaSimple"),
        )

class ProductoVentaGateway(Protocol):
    "Protocolo para interacción con productos de venta en Xubio."
    def get_producto_venta(self, updated_since: Optional[str] = None) -> List[ProductoVenta]:
        "Lista productos de venta desde Xubio, opcionalmente filtrando por fecha de actualización"
        pass # pylint: disable=unnecessary-pass

    def get_producto_ventaby_id(self, productoid: int) -> ProductoVenta:
        "Obtiene un producto de venta específico por ID desde Xubio"
        pass # pylint: disable=unnecessary-pass
