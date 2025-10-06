"""
Path: src/entities/cliente.py
"""

from typing import Optional, List, Protocol

class Cliente:
    "Entidad que representa un cliente en el dominio, extendida para Xubio /clienteBean"
    def __init__(
        self,
        cliente_id: str,
        nombre: str,
        primer_apellido: Optional[str] = None,
        segundo_apellido: Optional[str] = None,
        primer_nombre: Optional[str] = None,
        otros_nombres: Optional[str] = None,
        razon_social: Optional[str] = None,
        nombre_comercial: Optional[str] = None,
        identificacion_tributaria: Optional[dict] = None,
        digito_verificacion: Optional[str] = None,
        categoria_fiscal: Optional[dict] = None,
        provincia: Optional[dict] = None,
        direccion: Optional[str] = None,
        email: Optional[str] = None,
        telefono: Optional[str] = None,
        codigo_postal: Optional[str] = None,
        cuenta_venta_id: Optional[dict] = None,
        cuenta_compra_id: Optional[dict] = None,
        pais: Optional[dict] = None,
        localidad: Optional[dict] = None,
        usr_code: Optional[str] = None,
        lista_precio_venta: Optional[dict] = None,
        descripcion: Optional[str] = None,
        es_cliente_extranjero: Optional[int] = None,
        es_proveedor: Optional[int] = None,
        cuit: Optional[str] = None,
        tipo_de_organizacion: Optional[dict] = None,
        responsabilidad_organizacion_item: Optional[list] = None,
        CUIT: Optional[str] = None,
        actualizado_en: Optional[str] = None,
    ):
        self.cliente_id = cliente_id
        self.nombre = nombre
        self.primer_apellido = primer_apellido
        self.segundo_apellido = segundo_apellido
        self.primer_nombre = primer_nombre
        self.otros_nombres = otros_nombres
        self.razon_social = razon_social
        self.nombre_comercial = nombre_comercial
        self.identificacion_tributaria = identificacion_tributaria
        self.digito_verificacion = digito_verificacion
        self.categoria_fiscal = categoria_fiscal
        self.provincia = provincia
        self.direccion = direccion
        self.email = email
        self.telefono = telefono
        self.codigo_postal = codigo_postal
        self.cuenta_venta_id = cuenta_venta_id
        self.cuenta_compra_id = cuenta_compra_id
        self.pais = pais
        self.localidad = localidad
        self.usr_code = usr_code
        self.lista_precio_venta = lista_precio_venta
        self.descripcion = descripcion
        self.es_cliente_extranjero = es_cliente_extranjero
        self.es_proveedor = es_proveedor
        self.cuit = cuit
        self.tipo_de_organizacion = tipo_de_organizacion
        self.responsabilidad_organizacion_item = responsabilidad_organizacion_item
        self.CUIT = CUIT
        self.actualizado_en = actualizado_en

    @classmethod
    def from_dict(cls, data: dict):
        "Crea una instancia de Cliente desde un diccionario según el modelo oficial de Xubio"
        return cls(
            cliente_id=str(data.get("cliente_id") or data.get("id") or data.get("codigo") or ""),
            nombre=data.get("nombre") or data.get("primerNombre") or "",
            primer_apellido=data.get("primerApellido"),
            segundo_apellido=data.get("segundoApellido"),
            primer_nombre=data.get("primerNombre"),
            otros_nombres=data.get("otrosNombres"),
            razon_social=data.get("razonSocial"),
            nombre_comercial=data.get("nombreComercial"),
            identificacion_tributaria=data.get("identificacionTributaria"),
            digito_verificacion=data.get("digitoVerificacion"),
            categoria_fiscal=data.get("categoriaFiscal"),
            provincia=data.get("provincia"),
            direccion=data.get("direccion"),
            email=data.get("email"),
            telefono=data.get("telefono"),
            codigo_postal=data.get("codigoPostal"),
            cuenta_venta_id=data.get("cuentaVenta_id"),
            cuenta_compra_id=data.get("cuentaCompra_id"),
            pais=data.get("pais"),
            localidad=data.get("localidad"),
            usr_code=data.get("usrCode"),
            lista_precio_venta=data.get("listaPrecioVenta"),
            descripcion=data.get("descripcion"),
            es_cliente_extranjero=data.get("esclienteextranjero"),
            es_proveedor=data.get("esProveedor"),
            cuit=data.get("cuit"),
            tipo_de_organizacion=data.get("tipoDeOrganizacion"),
            responsabilidad_organizacion_item=data.get("responsabilidadOrganizacionItem"),
            CUIT=data.get("CUIT"),
            actualizado_en=data.get("updated_at") or data.get("actualizado_en"),
        )


class ClienteGateway(Protocol):
    " Puerto que define las operaciones para interactuar con clientes"
    def listar_clientes(self, updated_since: Optional[str] = None) -> List[Cliente]:
        "Lista clientes desde el sistema"
        pass  # pylint: disable=unnecessary-pass
